from analysis_suite.commons.histogram import Histogram
from analysis_suite.commons.plot_utils import darkenColor

import numpy as np

class Stack(Histogram):
    def __init__(self, bin_info):
        super().__init__("", bin_info)
        self.stack = list()
        self.options = {"stacked": True, "histtype": "stepfilled"}

    def __iadd__(self, right):
        idx = self._get_index(right.integral())
        self.stack.insert(idx, right)
        return super().__iadd__(right)

    def _get_index(self, integral):
        if not self.stack:
            return 0
        else:
            return np.argmax(np.array([s.integral() for s in self.stack]) < integral)

    def plot_stack(self, pad, **kwargs):
        n, bins, patches = pad.hist(
            weights=np.array([h.vals for h in self.stack]).T, bins=self.axis.edges,
            x=np.tile(self.axis.centers, (len(self.stack), 1)).T,
            color=[h.color for h in self.stack],
            label=[h.name for h in self.stack],
            **self.options, **kwargs
        )
        # Apply patch to edge colors
        edgecolors = [darkenColor(h.color) for h in self.stack]
        for p, ec in zip(patches, edgecolors):
            p[0].set_ec(ec)
