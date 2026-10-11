import bpy,json,sys
from pathlib import Path
result={'file':bpy.data.filepath,'texts':[{ 'name':t.name,'text':t.as_string()} for t in bpy.data.texts],'objects':[]}
for o in bpy.data.objects:
 d={'name':o.name,'type':o.type,'custom':{k:str(v) for k,v in o.items()},'location':list(o.location),'scale':list(o.scale)}
 if o.type=='FONT':d['body']=o.data.body
 if o.type=='MESH':
  d.update(vertices=len(o.data.vertices),edges=len(o.data.edges),faces=len(o.data.polygons),materials=[m.name for m in o.data.materials if m],xyz=[list(v.co) for v in o.data.vertices],polygons=[list(p.vertices) for p in o.data.polygons])
 result['objects'].append(d)
path=Path(bpy.data.filepath).with_suffix('.json');path.write_text(json.dumps(result))
print('CTF_AUDIT',json.dumps({**result,'objects':[{k:v for k,v in x.items() if k not in ['xyz','polygons']} for x in result['objects']]}))
