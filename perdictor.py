import ephem

class predictor():
    def __init__(self):
        self.me = ephem.Observer()
        self.me.lon, self.me.lat, self.me.elevation = '116.682853', '40.415382', 0
        self.tle_path = "./tle.txt"

        f = open(self.tle_path)
        while True:
            line1=f.readline()
            if line1 == '':
                break
            line2=f.readline()
            line3=f.readline()
            print(line1,line2,line3)
            
        f.close()

        # sat = ephem.readtle(self.line1, self.line2, self.line3)
        # self.me.date = ephem.now()
        # sat.compute(self.me)

a=predictor()