import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

style.use('bmh')
fig, axes = plt.subplots(nrows=2, ncols=2)
ax1, ax2, ax3, ax4 = axes.flatten()

def animate(i):
	data = open('data.txt', 'r').read()
	lines = data.split('\n')
	times = []
	flux = []
	skyTemp = []
	ambTemp = []
	dhtTemp = []
	humidity = []
	for line in lines:
		if len(line) >1:
			d, t, f, h, sT, aT, dT = [x for x in line.split(' ')]
			t = datetime.datetime.strptime(d+' ' +t, "%Y-%m-%d %H:%M:%S")
			times.append(t)
			flux.append(float(f))
			skyTemp.append(float(sT))
			ambTemp.append(float(aT))
			dhtTemp.append(float(dT))
			humidity.append(float(h))
	ax1.clear()
	ax2.clear()
	ax3.clear()
	ax4.clear()
	ax1.plot(times, skyTemp, 'C0')
	ax2.plot(times, humidity, 'C1')
	ax3.plot(times, flux, 'navy')
	ax4.plot(times, dhtTemp, 'C3')
	ax4.plot(times, ambTemp, 'C4')
	ax1.grid(True)
	ax2.grid(True)
	ax3.grid(True)
	ax4.grid(True)
	ax1.set_title('Sky temperature, $^\circ$C')
	ax2.set_title('Humidity, \%')
	ax3.set_title('Flux, lux')
	ax4.set_title('Temperature, $^\circ$C')
	plt.gcf().autofmt_xdate()

ani = animation.FuncAnimation(fig, animate, interval = 1000)
fig.tight_layout()
plt.show()