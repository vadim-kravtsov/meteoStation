#!/usr/bin/python

from math import isnan, exp, log
import warnings
import datetime
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.image as mpimg
#import matplotlib.animation as animation
from matplotlib import style, cm
from os import popen, system

def dew_point(t, h):
    """Calc dew point"""
    a, b, c, d = (6.1, 18.7, 257.1, 234.5)
    def g(t, h):
        return log(h/100.0*exp((b-t/d)*(t/(c+t))))
    return c*g(t,h)/(b-g(t,h))

def dew_line(T, H):
    """Calc dew line"""
    return [dew_point(t, h) for t, h in zip(T, H)]

lines = open('/home/meteo/data/data.txt', 'r').readlines()
#lines = open('data.txt', 'r').readlines()
#if len(lines) >= 2880:
#    date = datetime.datetime.now().strftime("%Y%m%d")
#    archiveData = open('/home/meteo/data/archive/%s.txt'%date, 'w')
#    for line in lines[-1440:]:
#        archiveData.write(str(line))
#    archiveData.close()
times = []
flux = []
skyTemp = []
inTemp = []
outTemp = []
humidity = []
time_now = datetime.datetime.now()
for line in lines:
    if len(line) > 1:
        d, t = line.split()[:2]
        #outH, outT, inH, inT, irT, skyT
        oH, oT, iH, iT, irT, sT = [float(x) for x in line.split()[2:]]
#       if isnan(f) or isnan(h) or isnan(sT) or isnan(oT) or isnan(iT) or isnan(h):
#            continue
        t = datetime.datetime.strptime(d+' '+t, "%Y-%m-%d %H:%M:%S")
        seconds_from_now = (time_now - t).total_seconds()
        if seconds_from_now <= 86400:
            # Include only points within last day
            times.append(seconds_from_now)
            if oT >= 0:
                skyTemp.append(sT-abs(irT))
            else:
                skyTemp.append(sT+abs(irT))
            inTemp.append(iT)
            outTemp.append(oT)
            humidity.append(oH)
# Show ticks labels at the beginnings of all hours
beginning_of_hour = time_now.replace(minute=0, second=0)
seconds_from_beginning_of_hour = (time_now-beginning_of_hour).total_seconds()
ticks_locations = []
ticks_labels = []
for delta_hours in range(0, 24, 2):
    ticks_locations.append(3600 * delta_hours + seconds_from_beginning_of_hour)
    hour_to_show = time_now.hour - delta_hours
    if hour_to_show < 0:
        hour_to_show += 24
    ticks_labels.append("%i:00" % hour_to_show)

# make plots now
style.use('bmh')
fig = plt.figure(figsize = (7,14))

font = {'family': 'sans',
        'weight': 'normal',
        }

#plot current values
#uptime = popen('ps -eo args,etime|grep meteoStation.py').read().split()[-1]
#ut = uptime.split('-')
#uptime = "%s day and %s"%(ut[0],ut[1]) if len(ut)==2 else 0
gs0 = gridspec.GridSpec(1, 1)
header = fig.add_subplot(gs0[0], xticks = [], yticks = [])
header.set_ylim(100,0)
header.set_xlim(0,100)
header.patch.set_visible(False)
#header.text(2,75,'last update: %s '%t, fontdict = font, fontsize = 12)
#if uptime:
#    header.text(22,75,'uptime: %s'%uptime, fontdict = font, fontsize = 12)
if skyTemp[-1]>0.2:
    header.text(6, 75, 'WARNING! CLOUD SENSOR MAY BE COVERED BY SNOW/WATER!', fontdict = font, fontsize = 12, color = 'red')
    #header.text(20, 75, 'BETA TESTING! WEATHER IN 3104', fontdict = font, fontsize = 12, color = 'red')
else:
    header.text(3, 75, 'last update: %s'%(datetime.datetime.strftime(time_now, '%H:%M')), fontdict = font, fontsize = 12)
    #header.text(43, 75, 'WEATHER IN 3104', fontdict = font, fontsize = 12, color = 'red')
header.grid(False)
with warnings.catch_warnings():
    warnings.simplefilter("ignore", UserWarning)
    gs0.tight_layout(fig, rect=[0.051, 0.960, 0.99, None])


#plot h-level
gs1 = gridspec.GridSpec(1, 4)
tx1 = fig.add_subplot(gs1[0], xticks = [], yticks = [])
h = humidity[-1]
c = ("#FF5353" if h>80 else ("#FFBE28" if h>60 else "#2DC800"))
tx1.fill([0,0,1,1],[0,h,h,0], color = c)
tx1.hlines(h, 0, 1,color = 'grey', linewidth = 1)
tx1.text(0.5, h/2-8, '%1.1f%%'%h, fontdict = font, horizontalalignment='center', fontsize=20)
#tx1.text(0.5, h/2-10, 'high :)', fontdict = font, horizontalalignment='center', fontsize=20)
tx1.set_title('humidity')
tx1.set_ylim(0,100)
tx1.set_xlim(0,1)
tx1.grid(False)

#plot temperature
tx2 = fig.add_subplot(gs1[1], xticks = [], yticks = [])
tx2.set_title('temperature')
t = outTemp[-1] 
c = '#fc913a' if t>10 else ('#3b74bf' if t<-10 else ('#a0ccff' if t<0 else '#ECDB54'))
tx2.fill([0,0,1,1],[0,100,100,0], color = c)
tx2.text(0.5, 40, '%1.1f$^\circ$C'%t, fontdict = font, horizontalalignment='center', fontsize=20)
tx2.set_ylim(0,100)
tx2.set_xlim(0,1)


#plot cloudiness value

tx3 = fig.add_subplot(gs1[2], xticks = [], yticks = [])
tx3.set_title('cloudiness')
s = skyTemp[-1]
cmap = ["#2DC800", "#32DF00", "#DFDF00", "#F9BB00", "#FF800D", "#ff4e50"]
if s>-1:
    c_value = 5
elif -5<s<-1:
    c_value = 4
elif -10<s<-5:
    c_value = 3
elif -15<s<-10:
    c_value = 2
elif -20<s<-15:
    c_value = 1
elif s<-20:
    c_value = 0
tx3.fill([0,0,1,1],[0,100,100,0], color = cmap[c_value])
tx3.text(0.5, 40, '%i'%c_value, fontdict = font, horizontalalignment='center', fontsize=20)
tx3.set_ylim(0,100)
tx3.set_xlim(0,1)

#plot dew pointw
tx4 = fig.add_subplot(gs1[3], xticks = [], yticks = [])
tx4.set_title('dew point')
dp = dew_point(t, h)
tx4.fill([0,0,1,1],[0,100,100,0], color = "#8ED6EA")
tx4.text(0.5, 40, '%1.1f$^\circ$C'%dp, fontdict = font, horizontalalignment='center', fontsize=20)
tx4.set_ylim(0,100)
tx4.set_xlim(0,1)


with warnings.catch_warnings():
    warnings.simplefilter("ignore", UserWarning)
    gs1.tight_layout(fig, rect=[0.051, 0.820, 0.99, 0.960])


gs2 = gridspec.GridSpec(4, 1)
ax1 = fig.add_subplot(gs2[0])
ax2 = fig.add_subplot(gs2[1])
ax3 = fig.add_subplot(gs2[2])
ax4 = fig.add_subplot(gs2[3])
#ax5 = fig.add_subplot(gs2[4])

# plot sky temperature for last hour
ax1.clear()
ax1.set_ylim(-35,10)
ax1.set_xlim(left=3600, right=0)
ax1.set_xticks(range(3600, -1, -300))
ax1.set_xticklabels([str(m) for m in range(60,-5, -5)])
ax1.plot(times, skyTemp, 'C7')
ax1.axhline(0, linestyle = 'dashed', linewidth = 1, color = 'r', label = 'cloudy')
ax1.axhline(-12.5, linestyle = 'dashed', linewidth = 1, color = 'y', label = 'partly cloudless')
ax1.axhline(-25, linestyle = 'dashed', linewidth = 1, color = 'g', label = 'cloudless')
ax1.legend(framealpha = 1, facecolor = 'w')
ax1.grid(True)
ax1.set_title('Relative sky temperature [1h], $^\circ$C')

# plot sky temperature for 24 hours
ax2.clear()
ax2.set_ylim(-35, 10)
ax2.set_xlim(left=86400, right=0)
ax2.set_xticks(ticks_locations)
ax2.set_xticklabels(ticks_labels)
ax2.plot(times, skyTemp, 'C0')
ax2.axhline(0, linestyle = 'dashed', linewidth = 1, color = 'r', label = 'cloudy')
ax2.axhline(-12.5, linestyle = 'dashed', linewidth = 1, color = 'y', label = 'partly cloudless')
ax2.axhline(-25, linestyle = 'dashed', linewidth = 1, color = 'g', label = 'cloudless')
ax2.grid(True)
ax2.set_title('Relative sky temperature [24 h], $^\circ$C')

# plot humidity
ax3.clear()
ax3.set_xlim(left=86400, right=0)
ax3.set_xticks(ticks_locations)
ax3.set_xticklabels(ticks_labels)
ax3.plot(times, humidity, 'C1')
ax3.grid(True)
ax3.set_title('Humidity, %')

# plot flux
#ax4.clear()
#ax4.set_xlim(left=86400, right=0)
#ax4.set_xticks(ticks_locations)
#ax4.set_xticklabels(ticks_labels)
#ax4.plot(times, flux, 'navy')
#ax4.set_yscale('symlog')  # logarithmic scale for the flux
#ax4.grid(True)
#ax4.set_title('Flux, lux')

# plot ambient temperature
ax4.clear()
ax4.set_xlim(left=86400, right=0)
ax4.set_xticks(ticks_locations)
ax4.set_xticklabels(ticks_labels)
ax4.plot(times, outTemp, 'C3', label = 'outside', linewidth = 2.5)
ax4.axhline(0,linestyle = 'dashed', linewidth = 1, color = 'y')
ax4.plot(times, dew_line(outTemp, humidity),
                         linewidth = 1, color = 'C5', label = 'dew point')
#ax4.plot(times, inTemp, 'C2', label = 'infrared (in the box)')
ax4.set_title('Temperature, $^\circ$C')
ax4.legend()
ax4.grid(True)

#ani = animation.FuncAnimation(fig, animate, interval = 10000)
with warnings.catch_warnings():
    warnings.simplefilter("ignore", UserWarning)
    gs2.tight_layout(fig, rect=[None, None, None, 0.820])

#plt.show()
plt.savefig('/home/meteo/data/meteo_plot.svg', format='svg')
#plt.savefig('meteo_plot.svg', format='svg')

if abs((time_now - time_now.replace(hour = 0, minute = 0, second = 0, microsecond = 0)).total_seconds()) < 300:
    date = datetime.datetime.now().strftime("%Y%m%d")
    archiveData = open('/home/meteo/data/archive/%s.txt'%date, 'w')
    lastData = open('/home/meteo/data/data1.txt', 'w')
    for line in lines:
        if len(line) > 1:
            d, t = line.split()[:2]
            t = datetime.datetime.strptime(d+' '+t, "%Y-%m-%d %H:%M:%S")
            seconds_from_now = (time_now - t).total_seconds()
            if seconds_from_now <= 172800:
                lastData.write(line)
                if seconds_from_now <= 86400:
                    archiveData.write(line)
    archiveData.close()
    lastData.close()
    system('cp data1.txt data.txt')