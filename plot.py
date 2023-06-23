with open("result2023-06-20_17_32_35.txt", "r") as f:
    lines = f.readlines()
    
    newfile = open(f.name + ".kml", "w")
    newfile.write("<?xml version='1.0' encoding='UTF-8'?>\n<kml xmlns:ns=\"http://earth.google.com/kml/2.0\">\n  <Folder>\n    <open>1</open>")
    
    
    for line in lines:
        counte = 0
        line = line.replace('(', '')
        line = line.replace(')', '')
        line = line.replace(' ', '')
        a = line.split(',')
        for i in range(2, len(a)-1, 2):
            y = a[i]
            x = a[i+1]
            old_y = a[i-2]
            old_x = a[i-1]
            newfile.write("<Placemark>\n      <Point>\n        <coordinates>" + x + ", " + y + "</coordinates>\n      </Point>\n    </Placemark>\n    <Placemark>\n      <Point>\n        <coordinates>" + old_x + ", " + old_y + "</coordinates>\n      </Point>\n    </Placemark>\n    <Placemark>\n      <LineString>\n        <extrude>1</extrude>\n        <tessellate>1</tessellate>\n        <coordinates>"+ x + ", " + y + ",0" + old_x + ", " + old_y + "</coordinates>\n      </LineString>\n    </Placemark>")
    newfile.write("  </Folder>\n</kml>")

            
