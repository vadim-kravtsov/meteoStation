import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig, axes = plt.subplots(nrows=2, ncols=2)
ax1, ax2, ax3, ax4 = axes.flatten()

def animate(i):
	data = open('data.txt', 'r').read()
	lines = data.split('\n')
	time = []
	flux = []
	skyTemp = []
	ambTemp = []
	dhtTemp = []
	humidity = []
	for line in lines:
		if len(line) >1:
			t, f, h, sT, aT, dT = [float(x) for x in line.split(' ')]
			time.append(t)
			flux.append(f)
			skyTemp.append(sT)
			ambTemp.append(aT)
			dhtTemp.append(dT)
			humidity.append(h)
	ax1.clear()
	ax2.clear()
	ax3.clear()
	ax4.clear()
	ax1.plot(time, skyTemp)
	ax2.plot(time, humidity)
	ax3.plot(time, flux)
	ax4.plot(time, dhtTemp)
	ax1.grid(True)
	ax2.grid(True)
	ax3.grid(True)
	ax4.grid(True)
	ax1.set_title('SkyTemp')
	ax2.set_title('Humidity')
	ax3.set_title('Flux')
	ax4.set_title('Temperature')
ani = animation.FuncAnimation(fig, animate, interval = 1000)
fig.tight_layout()
plt.show()