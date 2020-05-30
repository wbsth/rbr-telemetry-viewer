from lib.mplcanvas import MplCanvas
from numpy import ones, histogram
from matplotlib.ticker import PercentFormatter


class MapView(MplCanvas):
    def __init__(self, data, option):
        super(MapView, self).__init__(self)
        self._data = data
        self.plot()

    def plot(self):
        self.axes.plot(self._data['position.x'], self._data['position.y'], color='k', linewidth=1)
        self.axes.plot(self._data['position.x'][0], self._data['position.y'][0], marker='o', markersize=3, color="red")
        self.axes.xaxis.set_visible(False)
        self.axes.yaxis.set_visible(False)
        self.fig.set_tight_layout(True)

    def upd(self, slider_value):
        self.axes.lines.remove(self.axes.lines[-1])
        self.axes.plot(self._data['position.x'][slider_value], self._data['position.y'][slider_value], marker='o', markersize=3, color="red")
        self.draw()


class SuspHistogram(MplCanvas):
    def __init__(self, data, option):
        super(SuspHistogram, self).__init__(self)
        self._option = option
        self._data = data[f"{self._option[1]}.deflectionVelocity"]
        self.fbump, self.bump, self.rebound, self.frebound, self.binlist = self.calculate()
        self.plot()

    def calculate(self):
        # calculate percentages
        ranges = [-1, -0.3, 0, 0.3, 1]
        samples_number = len(self._data)
        vals, bins = histogram(self._data, ranges)
        percentages = (vals/samples_number)*100
        fbump, bump, rebound, frebound = percentages
        binlist = [x / 1000.0 for x in range(-1025, 1025, 50)]
        return fbump, bump, rebound, frebound, binlist

    def plot(self):
        # plot histogram
        self.axes.hist(self._data, range=(-1, 1), bins=self.binlist, weights=ones(len(self._data)) / len(self._data))

        # draw text
        self.axes.text(0.1, 0.85, f'f_bump\n{self.fbump:.2f}%', horizontalalignment='left', transform=self.axes.transAxes)
        self.axes.text(0.4, 0.85, f'bump\n{self.bump:.2f}%', horizontalalignment='left', transform=self.axes.transAxes)
        self.axes.text(0.53, 0.85, f'rebound\n{self.rebound:.2f}%', horizontalalignment='left',
                       transform=self.axes.transAxes)
        self.axes.text(0.8, 0.85, f'f_rebound\n{self.frebound:.2f}%', horizontalalignment='left',
                       transform=self.axes.transAxes)

        # draw vertical lines separating areas
        for i in [-0.3, 0, 0.3]:
            self.axes.axvline(i, color='k', linestyle='dashed', linewidth=1)

        # set y-axis to percentages
        self.axes.yaxis.set_major_formatter(PercentFormatter(1))

        self.fig.set_tight_layout(True)

    def upd(self, slider_value):
        pass


class TireTemps(MplCanvas):
    def __init__(self, data, option):
        super(TireTemps, self).__init__(self)
        self._data = data
        self._option = option
        self._temp_coef = 273
        self.plot()

    def plot(self):
        for i in ['LF', 'RF', 'LB', 'RB']:
            self.axes.plot(self._data[f"{i}.tyreTemperature"]-self._temp_coef, label=f"{i}")
        self.axes.axvline(0, color='r')
        self.axes.set_ylabel("Tire temp [C]")
        self.axes.legend(loc='upper left')
        self.fig.set_tight_layout(True)

    def upd(self, slider_value):
        self.axes.lines.remove(self.axes.lines[-1])
        self.axes.axvline(slider_value, color='r')
        self.draw()
