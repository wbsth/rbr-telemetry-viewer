from lib.mplcanvas import MplCanvas


class SimpleGraph(MplCanvas):
    def __init__(self, data, option):
        super(SimpleGraph, self).__init__(self)
        self._data = data
        self._option = option
        self.axes.plot(self._data[self._option], color='k', linewidth=1)
        self.axes.axvline(list(self._data.index.values)[0], color='r', label='-')
        self.axes.legend(loc='upper right')
        self.fig.set_tight_layout(True)

    def upd(self, slider_value):
        # remove old vertical line
        self.axes.lines.remove(self.axes.lines[-1])
        # add new vertical line
        value = self._data[self._option][slider_value]
        # format legend str
        if isinstance(value, float):
            str_value = "{:.2f}".format(value)
        else:
            str_value = str(value)
        # add new vertical line
        self.axes.axvline(slider_value, color='r', label=str_value)
        self.axes.legend(loc='upper right')
        # redraw
        self.draw()
