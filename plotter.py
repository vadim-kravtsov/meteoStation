from math import isnan, exp, log
import warnings
import datetime
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
#import matplotlib.animation as animation
from matplotlib import style

def dew_point(t, h):
    """Calc dew point"""
    a, b, c, d = (6.1, 18.7, 257.1, 234.5)
    def g(t, h):
        return log(h/100.0*exp((b-t/d)*(t/(c+t))))
    return c*g(t,h)/(b-g(t,h))

def dew_line(T, H):
    """Calc dew line"""
    return [dew_point(t, h) for t, h in zip(T, H)]

lines = open('data.txt', 'r').readlines()
if len(lines) >= 2880:
    date = datetime.datetime.now().strftime("%Y%m%d")
    archiveData = open('archive/%s.txt'%date, 'w')
    for line in lines[:-1440]:
        archiveData.write(str(line))
    archiveData.close()
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
        f, h, sT, iT, oT = [float(x) for x in line.split()[2:]]
        if f <= 5:
            f = 0
        if isnan(f) or isnan(h) or isnan(sT) or isnan(oT) or isnan(iT) or isnan(h):
            continue
        t = datetime.datetime.strptime(d+' '+t, "%Y-%m-%d %H:%M:%S")
        seconds_from_now = (time_now - t).total_seconds()
        if seconds_from_now <= 86400:
            # Include only points within last day
            times.append(seconds_from_now)
            flux.append(f)
            skyTemp.append(sT-oT)
            inTemp.append(iT)
            outTemp.append(oT)
            humidity.append(h)
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



#plot current values
gs1 = gridspec.GridSpec(1, 4)
tx1 = fig.add_subplot(gs1[0])
tx2 = fig.add_subplot(gs1[1])
tx3 = fig.add_subplot(gs1[2])
tx4 = fig.add_subplot(gs1[3])

with warnings.catch_warnings():
    warnings.simplefilter("ignore", UserWarning)
    # This raises warnings since tight layout cannot
    # handle gridspec automatically. We are going to
    # do that manually so we can filter the warning.
    gs1.tight_layout(fig, rect=[None, 0.875, None, None])


gs2 = gridspec.GridSpec(5, 1)
ax1 = fig.add_subplot(gs2[0])
ax2 = fig.add_subplot(gs2[1])
ax3 = fig.add_subplot(gs2[2])
ax4 = fig.add_subplot(gs2[3])
ax5 = fig.add_subplot(gs2[4])

# plot sky temperature for last hour
ax1.clear()
ax1.set_xlim(left=3600, right=0)
ax1.set_xticks(range(3600, -1, -300))
ax1.set_xticklabels([str(m) for m in range(0, 61, 5)])
ax1.plot(times, skyTemp, 'C7')
ax1.hlines(-5, times[0], times[-1], linestyles = 'dashed', linewidth = 1,
                         colors = 'r', label = 'cloudy')
ax1.hlines(-15, times[0], times[-1], linestyles = 'dashed', linewidth = 1,
                         colors = 'y', label = 'partly cloudless')
ax1.hlines(-25, times[0], times[-1], linestyles = 'dashed', linewidth = 1,
                         colors = 'g', label = 'cloudless')
ax1.legend(framealpha = 1, facecolor = 'w')
ax1.grid(True)
ax1.set_title('Relative sky temperature [1h], $^\circ$C')

# plot sky temperature for 24 hours
ax2.clear()
ax2.set_xlim(left=86400, right=0)
ax2.set_xticks(ticks_locations)
ax2.set_xticklabels(ticks_labels)
ax2.plot(times, skyTemp, 'C0')
ax2.hlines(-5, times[0], times[-1], linestyles = 'dashed', linewidth = 1,
                         colors = 'r', label = 'cloudy')
ax2.hlines(-15, times[0], times[-1], linestyles = 'dashed', linewidth = 1,
                         colors = 'y', label = 'partly cloudless')
ax2.hlines(-25, times[0], times[-1], linestyles = 'dashed', linewidth = 1,
                         colors = 'g', label = 'cloudless')
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
ax4.clear()
ax4.set_xlim(left=86400, right=0)
ax4.set_xticks(ticks_locations)
ax4.set_xticklabels(ticks_labels)
ax4.plot(times, flux, 'navy')
ax4.set_yscale('symlog')  # logarithmic scale for the flux
ax4.grid(True)
ax4.set_title('Flux, lux')

# plot ambient temperature
ax5.clear()
ax5.set_xlim(left=86400, right=0)
ax5.set_xticks(ticks_locations)
ax5.set_xticklabels(ticks_labels)
ax5.plot(times, outTemp, 'C3', label = 'outside', linewidth = 2.5)
ax5.plot(times, dew_line(outTemp, humidity),
                         linewidth = 1, color = 'C5', label = 'dew point')
#ax5.plot(times, inTemp, 'C1', label = 'inside')
ax5.set_title('Temperature, $^\circ$C')
ax5.legend()
ax5.grid(True)

#ani = animation.FuncAnimation(fig, animate, interval = 10000)
with warnings.catch_warnings():
    warnings.simplefilter("ignore", UserWarning)
    # This raises warnings since tight layout cannot
    # handle gridspec automatically. We are going to
    # do that manually so we can filter the warning.
    gs2.tight_layout(fig, rect=[None, None, None, 0.875])

#plt.show()
plt.savefig('meteo_plot.svg')
