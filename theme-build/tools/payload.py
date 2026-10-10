# Build a themeFilesUpsert variables JSON for given files and print it (compact).
import json, sys
files=[{"filename":f,"body":{"type":"TEXT","value":open('src/'+f,encoding='utf-8').read()}} for f in sys.argv[1:]]
print(json.dumps({"themeId":"gid://shopify/OnlineStoreTheme/186651934933","files":files},ensure_ascii=False))
