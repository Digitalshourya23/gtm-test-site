import dns.resolver, json, ipaddress, sys, concurrent.futures as cf
R=dns.resolver.Resolver(); R.lifetime=6; R.timeout=3
rng=json.load(open('ip-ranges.json'))
nets=[]
for p in rng['prefixes']:
    nets.append((ipaddress.ip_network(p['ip_prefix']),p['region'],p['service']))
# collapse: map to most specific non-AMAZON service
def aws_ip(ip):
    a=ipaddress.ip_address(ip); best=None
    for n,reg,svc in nets:
        if a in n:
            if best is None or (best[1]=='AMAZON' and svc!='AMAZON'): best=(reg,svc)
    return best
def q(name,t):
    try: return [x.to_text().rstrip('.') for x in R.resolve(name,t)]
    except Exception: return []
def chain(name):
    try:
        ans=R.resolve(name,'A')
        cn=[str(rr.target).rstrip('.') for rrset in ans.response.answer for rr in rrset if rr.rdtype==5]
        ips=[x.address for x in ans]
        return cn,ips
    except Exception: return [],[]
SUBS=['','www.','api.','app.','m.','cdn.','static.','images.','admin.','portal.','shop.','login.']
def check(dom):
    s={'domain':dom,'signals':[]}
    ns=q(dom,'NS')
    if any('awsdns' in n for n in ns): s['signals'].append('Route53-NS')
    txt=' '.join(q(dom,'TXT'))
    if 'amazonses' in txt: s['signals'].append('SES-SPF')
    mx=' '.join(q(dom,'MX'))
    if 'amazonaws' in mx or 'awsapps' in mx: s['signals'].append('AWS-MX')
    hosts=[]
    regions=set()
    for sub in SUBS:
        h=sub+dom; cn,ips=chain(h)
        if not ips: continue
        tags=set()
        c=' '.join(cn)
        if 'cloudfront.net' in c: tags.add('CloudFront')
        if 'elb.amazonaws.com' in c: tags.add('ELB')
        if 'awsglobalaccelerator' in c: tags.add('GlobalAccel')
        if 'elasticbeanstalk' in c: tags.add('Beanstalk')
        if 'amplifyapp' in c: tags.add('Amplify')
        if 's3' in c and 'amazonaws' in c: tags.add('S3')
        for ip in ips:
            b=aws_ip(ip)
            if b:
                tags.add('AWS-IP'); 
                if b[0]!='GLOBAL': regions.add(b[0])
        if tags: hosts.append(f"{h}:{'+'.join(sorted(tags))}")
        for t in tags:
            if t not in s['signals']: s['signals'].append(t)
    s['hosts']=hosts; s['regions']=sorted(regions)
    s['other_cdn']=[] 
    s['ns']=ns[:1]
    s['aws']=len(hosts)>0 or 'Route53-NS' in s['signals']
    return s
if __name__=='__main__':
    doms=[l.split()[0] for l in open(sys.argv[1]) if l.strip() and not l.startswith('#')]
    with cf.ThreadPoolExecutor(24) as ex:
        res=list(ex.map(check,doms))
    json.dump(res,open(sys.argv[2],'w'),indent=1)
    for r in res: print(r['domain'], 'AWS' if r['aws'] else '---', ','.join(r['signals']), r['regions'])
