import statistics as st
rows=[(2185,174.3),(2241,177.3),(2244,178.7),(2210,176.3),(2216,178.5),(2201,175.8),(2220,176),(2221,178.4),(2228,179.4),(2230,178),(2220,178.4),(2202,175.6),(2200,178.5),(2191,177.1),(2195,178),(2235,175.7),(2238,173.5),(2219,173.7),(2246,174.6),(2245,177.5),(2246,179.5),(2272,175.6),(2261,180),(2253,183.1),(2262,181.8)]
ks=[p/v for p,v in rows]
print(len(rows), sum(p for p,v in rows), sum(v for p,v in rows))
print('sum ratio', sum(p for p,v in rows)/sum(v for p,v in rows))
print('mean k', st.mean(ks), 'sd', st.stdev(ks), 'min', min(ks), 'max', max(ks))
print('median', st.median(ks))
print('mean pulses', st.mean(p for p,v in rows), 'mean ml', st.mean(v for p,v in rows))
for p,v in rows: print(p,v,round(p/v,3))
