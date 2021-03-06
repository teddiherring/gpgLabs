import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
try:
    from IPython.html.widgets import  interact, interactive, IntSlider, widget, FloatText, FloatSlider
    pass
except Exception, e:    
    from ipywidgets import interact, interactive, IntSlider, widget, FloatText, FloatSlider


def ViewWiggle(syndata, obsdata):
    dx = 20
    fig, ax = plt.subplots(1, 2, figsize=(14, 8))
    kwargs = {
    'skipt':1,
    'scale': 0.05,
    'lwidth': 1.,
    'dx': dx,
    'sampr': 0.004,
    'clip' : dx*10.,
    }
    extent = [0., 38*dx, 1.0, 0.]

    ax[0].invert_yaxis()
    ax[1].invert_yaxis()
    wiggle(syndata, ax = ax[0], **kwargs)
    wiggle(obsdata, ax = ax[1], **kwargs)
    ax[0].set_xlabel("Offset (m)")
    ax[0].set_ylabel("Time (s)")
    ax[0].set_title("Clean CMP gather")
    ax[1].set_xlabel("Offset (m)")
    ax[1].set_ylabel("Time (s)")
    ax[1].set_title("Noisy CMP gather")

def NoisyNMOWidget(t0, v):
    syndata = np.load('obsdata1.npy')
    dx = 20
    xorig = np.arange(38)*dx
    time = HyperbolicFun(t0, xorig, v)
    # fig, ax = plt.subplots(1, 2, figsize=(14, 8))
    fig = plt.figure(figsize=(20, 8))
    kwargs = {
    'skipt':1,
    'scale': 0.05,
    'lwidth': 1.,
    'dx': dx,
    'sampr': 0.004,
    'clip' : dx*10.,
    }
    gs1 = gridspec.GridSpec(1, 9)
    gs1.update(left=0.05, right=0.48, wspace=0.05)
    ax1 = plt.subplot(gs1[:, 0:3])
    ax2 = plt.subplot(gs1[:, 4:7])
    ax3 = plt.subplot(gs1[:, 8])

    extent = [0., 38*dx, 1.0, 0.]
    ax1.invert_yaxis()
    ax2.invert_yaxis()
    wiggle(syndata, ax = ax1, **kwargs)
    toffset = np.sqrt(xorig**2/v**2+t0**2)-t0
    wiggle(syndata, ax = ax2, manthifts=toffset, **kwargs)

    ax1.axis(extent)
    ax2.axis(extent)    
    ax1.plot(xorig, time, 'r', lw=2)

    ax1.set_xlabel("Offset (m)")
    ax2.set_xlabel("Offset (m)")
    ax1.set_ylabel("Time (s)")
    ax2.set_ylabel("Time (s)")
    ax1.set_title("CMP gather")
    ax2.set_title("NMO corrected CMP gather")
    
    time_data = np.load('time1.npy')
    singletrace = NMOstack(syndata, xorig, time_data, v) 
    # singletrace = singletrace 

    kwargs = {
    'skipt':1,
    'scale': 2.,
    'lwidth': 1.,
    'sampr': 0.004,
    'ax': ax3,
    'clip' : 10,
    }
    extent = [singletrace.min(), singletrace.max(), time_data.max(), time_data.min()]
    ax3.invert_yaxis()
    ax3.axis(extent)
    wiggle(singletrace.reshape([1,-1]), **kwargs)
    ax3.set_xlabel("Amplitude")
    ax3.set_ylabel("Time (s)")
    ax3.set_xlim(-4.5, 4.5)
    ax3.set_xticks([-4.5, 0., 4.5])
    ax3.set_title("Stacked trace")

def CleanNMOWidget(t0, v):
    syndata = np.load('syndata1.npy')
    np.random.randn()
    dx = 20
    xorig = np.arange(38)*dx
    time = HyperbolicFun(t0, xorig, v)
    # fig, ax = plt.subplots(1, 2, figsize=(14, 8))
    fig = plt.figure(figsize=(20, 8))
    kwargs = {
    'skipt':1,
    'scale': 0.05,
    'lwidth': 1.,
    'dx': dx,
    'sampr': 0.004,
    'clip' : dx*10.,
    }
    gs1 = gridspec.GridSpec(1, 9)
    gs1.update(left=0.05, right=0.48, wspace=0.05)
    ax1 = plt.subplot(gs1[:, 0:3])
    ax2 = plt.subplot(gs1[:, 4:7])
    ax3 = plt.subplot(gs1[:, 8])

    extent = [0., 38*dx, 1.0, 0.]
    ax1.invert_yaxis()
    ax2.invert_yaxis()
    wiggle(syndata, ax = ax1, **kwargs)
    toffset = np.sqrt(xorig**2/v**2+t0**2)-t0
    wiggle(syndata, ax = ax2, manthifts=toffset, **kwargs)

    ax1.axis(extent)
    ax2.axis(extent)    
    ax1.plot(xorig, time, 'r', lw=2)

    ax1.set_xlabel("Offset (m)")
    ax2.set_xlabel("Offset (m)")
    ax1.set_ylabel("Time (s)")
    ax2.set_ylabel("Time (s)")
    ax1.set_title("CMP gather")
    ax2.set_title("NMO corrected CMP gather")
    
    time_data = np.load('time1.npy')
    singletrace = NMOstack(syndata, xorig, time_data, v) 
    # singletrace = singletrace 

    kwargs = {
    'skipt':1,
    'scale': 2.,
    'lwidth': 1.,
    'sampr': 0.004,
    'ax': ax3,
    'clip' : 10,
    }
    extent = [singletrace.min(), singletrace.max(), time_data.max(), time_data.min()]
    ax3.invert_yaxis()
    ax3.axis(extent)
    wiggle(singletrace.reshape([1,-1]), **kwargs)
    ax3.set_xlabel("Amplitude")
    ax3.set_ylabel("Time (s)")
    ax3.set_xlim(-4.5, 4.5)
    ax3.set_xticks([-4.5, 0., 4.5])
    ax3.set_title("Stacked trace")

def HyperbolicFun(t0, x, velocity):
    time = np.sqrt(x**2/velocity**2+t0**2)
    return time

def NMOstackthree(data, tintercept, v1, v2, v3):
    dx = 20.
    xorig = np.arange(38)*dx
    time = np.load('time1.npy')
    traces = np.zeros((3,time.size))
    vtemp = np.r_[v1, v2, v3]
    for itry in range(3):
        traces[itry,:] = NMOstack(data, xorig, time, vtemp[itry])

    fig, ax = plt.subplots(1, 3, figsize=(10, 8))
    kwargs = {
    'skipt':1,
    'scale': 2.,
    'lwidth': 1.,
    'sampr': 0.004,
    'clip' : 10,
    }
    for i in range(3):
        extent = [traces[i,:].min(), traces[i,:].max(), time.max(), time.min()]
        ax[i].invert_yaxis()
        ax[i].axis(extent)
        wiggle(traces[i,:].reshape([1,-1]), ax=ax[i], **kwargs)
        ax[i].set_xlabel("Amplitude")
        if i==0:
            ax[i].set_ylabel("Time (s)")
        ax[i].set_title(("Velocity = %6.1f")%(vtemp[i]))

def NMOstack(data, xorig, time, v):
    if np.isscalar(v):
        v = np.ones_like(time)*v
    Time = (time.reshape([1,-1])).repeat(data.shape[0], axis=0)
    singletrace = np.zeros(data.shape[1])
    for i in range(time.size):
        toffset = np.sqrt(xorig**2/v[i]**2+time[i]**2)
        Time = (time.reshape([1,-1])).repeat(data.shape[0], axis=0)
        Toffset = (toffset.reshape([-1,1])).repeat(data.shape[1], axis=1)
        indmin = np.argmin(abs(Time-Toffset), axis=1)
        singletrace[i] = (mkvc(data)[sub2ind(data.shape, np.c_[np.arange(data.shape[0]), indmin])]).sum()
    return singletrace

def NMOstackSingle(data, tintercept, v):
    dx = 20.
    xorig = np.arange(38)*dx
    time = np.load('time1.npy')
    singletrace = NMOstack(data, xorig, time, v)

    fig, ax = plt.subplots(1, 1, figsize=(7, 8))
    kwargs = {
    'skipt':1,
    'scale': 2.,
    'lwidth': 1.,
    'sampr': 0.004,
    'ax': ax,
    'clip' : 10,
    }
    extent = [singletrace.min(), singletrace.max(), time.max(), time.min()]
    ax.invert_yaxis()
    ax.axis(extent)
    wiggle(singletrace.reshape([1,-1]), **kwargs)
    ax.set_xlabel("Amplitude")
    ax.set_ylabel("Time (s)")


def clipsign (value, clip):
  clipthese = abs(value) > clip
  return value * ~clipthese + np.sign(value)*clip*clipthese

def wiggle (traces, skipt=1,scale=1.,lwidth=.1,offsets=None,redvel=0., manthifts=None, tshift=0.,sampr=1.,clip=10., dx=1., color='black',fill=True,line=True, ax=None):

  ns = traces.shape[1]
  ntr = traces.shape[0]
  t = np.arange(ns)*sampr
  timereduce = lambda offsets, redvel, shift: [float(offset) / redvel + shift for offset in offsets]

  if (offsets is not None):
    shifts = timereduce(offsets, redvel, tshift)
  elif (manthifts is not None):
    shifts = manthifts
  else:
    shifts = np.zeros((ntr,))

  for i in range(0, ntr, skipt):
    trace = traces[i].copy()
    trace[0] = 0
    trace[-1] = 0

    if ax == None:
      if (line):
        plt.plot(i*dx + clipsign(trace / scale, clip), t - shifts[i], color=color, linewidth=lwidth)
      if (fill):
        for j in range(ns):
          if (trace[j] < 0):
            trace[j] = 0
        plt.fill(i*dx + clipsign(trace / scale, clip), t - shifts[i], color=color, linewidth=0)
    else:
      if (line):
        ax.plot(i*dx + clipsign(trace / scale, clip), t - shifts[i], color=color, linewidth=lwidth)
      if (fill):
        for j in range(ns):
          if (trace[j] < 0):
            trace[j] = 0
        ax.fill(i*dx + clipsign(trace / scale, clip), t - shifts[i], color=color, linewidth=0)

def sub2ind(shape, subs):
    """
    Extracted from SimPEG for temporary use (https://github.com/simpeg)

    From the given shape, returns the index of the given subscript

    """
    if len(shape) == 1:
        return subs
    if type(subs) is not np.ndarray:
        subs = np.array(subs)
    if len(subs.shape) == 1:
        subs = subs[np.newaxis,:]
    assert subs.shape[1] == len(shape), 'Indexing must be done as a column vectors. e.g. [[3,6],[6,2],...]'
    inds = np.ravel_multi_index(subs.T, shape, order='F')
    return mkvc(inds)

def mkvc(x, numDims=1):
    """
    Extracted from SimPEG for temporary use (https://github.com/simpeg)

    Creates a vector with the number of dimension specified

    e.g.::

        a = np.array([1, 2, 3])

        mkvc(a, 1).shape
            > (3, )

        mkvc(a, 2).shape
            > (3, 1)

        mkvc(a, 3).shape
            > (3, 1, 1)

    """
    if type(x) == np.matrix:
        x = np.array(x)

    if hasattr(x, 'tovec'):
        x = x.tovec()

    assert isinstance(x, np.ndarray), "Vector must be a numpy array"

    if numDims == 1:
        return x.flatten(order='F')
    elif numDims == 2:
        return x.flatten(order='F')[:, np.newaxis]
    elif numDims == 3:
        return x.flatten(order='F')[:, np.newaxis, np.newaxis]

def InteractClean():
    clean = interactive(CleanNMOWidget, t0 = (0.2, 0.8, 0.01), v = (1000., 5000., 100.))
    return clean 

def InteractNosiy():
    noisy = interactive(NoisyNMOWidget, t0 = (0.1, 0.6, 0.01),  v = (800., 2500., 100.))
    return noisy
