from math import isnan
import datetime
import matplotlib.pyplot as plt
#import matplotlib.animation as animation
from matplotlib import style

lines = open('/home/meteo/data/data.txt', 'r').readlines()
if len(lines) >= 2880:
    date = datetime.datetime.now().strftime("%Y%m%d")
    archiveData = open('/home/meteo/data/archive/%s.txt'%date, 'w')
    for line in lines[:-1440]:
        archiveData.write(str(line))
    archiveData.close()
times = []
flux = []
skyTemp = []
ambTemp = []
dhtTemp = []
humidity = []
time_now = datetime.datetime.now()
for line in lines:
    if len(line) > 1:
        d, t = line.split()[:2]
        f, h, sT, aT, dT = [float(x) for x in line.split()[2:]]
        if isnan(f) or isnan(h) or isnan(sT) or isnan(aT) or isnan(dT) or isnan(h):
            continue
        t = datetime.datetime.strptime(d+' '+t, "%Y-%m-%d %H:%M:%S")
        seconds_from_now = (time_now - t).total_seconds()
        if seconds_from_now <= 86400:
            # Include only points within last day
            times.append(seconds_from_now)
            flux.append(f)
            skyTemp.append(sT)
            ambTemp.append(aT)
            dhtTemp.append(dT)
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
fig, axes = plt.subplots(nrows=4, ncols=1, figsize = (7,10))
ax1, ax2, ax3, ax4 = axes.flatten()

# plot sky temperature
ax1.clear()
ax1.set_xlim(left=86400, right=0)
ax1.set_xticks(ticks_locations)
ax1.set_xticklabels(ticks_labels)
ax1.plot(times, skyTemp, 'C0')
ax1.grid(True)
ax1.set_title('Sky temperature, $^\circ$C')

# plot humidity
ax2.clear()
ax2.set_xlim(left=86400, right=0)
ax2.set_xticks(ticks_locations)
ax2.set_xticklabels(ticks_labels)
ax2.plot(times, humidity, 'C1')
ax2.grid(True)
ax2.set_title('Humidity, %')

# plot flux
ax3.clear()
ax3.set_xlim(left=86400, right=0)
ax3.set_xticks(ticks_locations)
ax3.set_xticklabels(ticks_labels)
ax3.plot(times, flux, 'navy')
ax3.set_yscale('symlog')  # logarithmic scale for the flux
ax3.grid(True)
ax3.set_title('Flux, lux')

# plot ambient temperature
ax4.clear()
ax4.set_xlim(left=86400, right=0)
ax4.set_xticks(ticks_locations)
ax4.set_xticklabels(ticks_labels)
ax4.plot(times, dhtTemp, 'C3')
ax4.set_title('Temperature, $^\circ$C')
ax4.grid(True)

#ani = animation.FuncAnimation(fig, animate, interval = 10000)
fig.tight_layout()
plt.savefig('/home/meteo/data/meteo_plot.svg')
