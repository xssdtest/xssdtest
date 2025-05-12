# cython: language_level=3
###############################################################################
 #    BSD LICENSE
 #
 #    Copyright (c) Saul Han <2573789168@qq.com>
 #
 #    Redistribution and use in source and binary forms, with or without
 #    modification, are permitted provided that the following conditions
 #    are met:
 #
 #       Redistributions of source code must retain the above copyright
 #        notice, this list of conditions and the following disclaimer.
 #       Redistributions in binary form must reproduce the above copyright
 #        notice, this list of conditions and the following disclaimer in
 #        the documentation and/or other materials provided with the
 #        distribution.
 #
 #    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 #    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 #    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 #    A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 #    OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 #    SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 #    LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 #    DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 #    THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 #    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 #    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
###############################################################################
from __future__ import print_function
from __future__ import print_function

import sys
import time
from math import log as _log, exp as _exp, pi as _pi, e as _e, ceil as _ceil
from math import sqrt as _sqrt, acos as _acos, cos as _cos, sin as _sin
from math import tau as TWOPI, floor as _floor, isfinite as _isfinite
from _collections_abc import Set as _Set, Sequence as _Sequence
from operator import index as _index
from itertools import accumulate as _accumulate, repeat as _repeat
from bisect import bisect as _bisect
sys.path.append("../")
from libc.stdlib cimport malloc
cimport xt_interface as interf

cdef interf.xt_lcg_random *g_xt_lcg_random

NV_MAGICCONST = 4 * _exp(-0.5) / _sqrt(2.0)
LOG4 = _log(4.0)
SG_MAGICCONST = 1.0 + _log(4.5)
BPF = 53        # Number of bits in a float
RECIP_BPF = 2 ** -BPF
_ONE = 1
XT_RAND_INIT = 0
XT_GAUSS_RAND_INIT = 0

cdef unsigned long long _rand_below(unsigned long long below):
    return interf.rand32() % below

cpdef unsigned long long xt_randint(unsigned long long start, unsigned long long stop, unsigned long long step = 1,
                                    unsigned long long aligned = 0xFFFFFFFFFFFFFFFF):
    """
    Args:
        start: 
        stop: 
        step: 
        aligned: 
    Returns: Return random integer in range [start, stop], including both end points.
    """
    cdef unsigned long long range = stop - start + 1
    cdef unsigned long long _rand = 0
    if step == 1:
        return (interf.rand64() % range + start) & aligned
    else:
        _rand = interf.rand64() % range
        _rand = _rand - _rand % step + start
        return _rand & aligned

cpdef double xt_uniform(double start, double stop):
    """
    Args:
        start: 
        stop: 
    Returns: return Get a random number in the range [a, b) or [a, b] depending on rounding.
    """
    return start + (stop - start) * interf.xt_random()


cpdef xt_triangular(double low=0.0, double high=1.0, mode=None):
    """Triangular distribution.

    Continuous distribution bounded by given lower and upper limits,
    and having a given mode value in-between.

    http://en.wikipedia.org/wiki/Triangular_distribution

    """
    cdef double u = interf.xt_random()
    cdef double c
    try:
        c = 0.5 if mode is None else (mode - low) / (high - low)
    except ZeroDivisionError:
        return low
    if u > c:
        u = 1.0 - u
        c = 1.0 - c
        low, high = high, low
    return low + (high - low) * _sqrt(u * c)

cpdef xt_choice(seq):
    """Choose a random element from a non-empty sequence."""
    return seq[_rand_below(len(seq))]


cpdef xt_sample(population, k, counts=None):
    """
    Chooses k unique random elements from a population sequence.

    Returns a new list containing elements from the population while
    leaving the original population unchanged.  The resulting list is
    in selection order so that all sub-slices will also be valid random
    samples.  This allows raffle winners (the sample) to be partitioned
    into grand prize and second place winners (the subslices).

    Members of the population need not be hashable or unique.  If the
    population contains repeats, then each occurrence is a possible
    selection in the sample.

    Repeated elements can be specified one at a time or with the optional
    counts parameter.  For example:

        sample(['red', 'blue'], counts=[4, 2], k=5)

    is equivalent to:

        sample(['red', 'red', 'red', 'red', 'blue', 'blue'], k=5)

    To choose a sample from a range of integers, use range() for the
    population argument.  This is especially fast and space efficient
    for sampling from a large population:

        sample(range(10000000), 60)

    """

    # Sampling without replacement entails tracking either potential
    # selections (the pool) in a list or previous selections in a set.

    # When the number of selections is small compared to the
    # population, then tracking selections is efficient, requiring
    # only a small set and an occasional reselection.  For
    # a larger number of selections, the pool tracking method is
    # preferred since the list takes less space than the
    # set and it doesn't suffer from frequent reselections.

    # The number of calls to _randbelow() is kept at or near k, the
    # theoretical minimum.  This is important because running time
    # is dominated by _randbelow() and because it extracts the
    # least entropy from the underlying random number generators.

    # Memory requirements are kept to the smaller of a k-length
    # set or an n-length list.

    # There are other sampling algorithms that do not require
    # auxiliary memory, but they were rejected because they made
    # too many calls to _randbelow(), making them slower and
    # causing them to eat more entropy than necessary.

    if not isinstance(population, _Sequence):
        raise TypeError("Population must be a sequence.  "
                        "For dicts or sets, use sorted(d).")
    n = len(population)
    if counts is not None:
        cum_counts = list(_accumulate(counts))
        if len(cum_counts) != n:
            raise ValueError('The number of counts does not match the population')
        total = cum_counts.pop()
        if not isinstance(total, int):
            raise TypeError('Counts must be integers')
        if total <= 0:
            raise ValueError('Total of counts must be greater than zero')
        selections = xt_sample(range(total), k=k)
        bisect = _bisect
        return [population[bisect(cum_counts, s)] for s in selections]
    if not 0 <= k <= n:
        raise ValueError("Sample larger than population or is negative")
    result = [None] * k
    setsize = 21        # size of a small set minus size of an empty list
    if k > 5:
        setsize += 4 ** _ceil(_log(k * 3, 4))  # table size for big sets
    if n <= setsize:
        # An n-length list is smaller than a k-length set.
        # Invariant:  non-selected at pool[0 : n-i]
        pool = list(population)
        for i in range(k):
            j = _rand_below(n - i)
            result[i] = pool[j]
            pool[j] = pool[n - i - 1]  # move non-selected item into vacancy
    else:
        selected = set()
        selected_add = selected.add
        for i in range(k):
            j = _rand_below(n)
            while j in selected:
                j = _rand_below(n)
            selected_add(j)
            result[i] = population[j]
    return result

cpdef xt_shuffle(x):
    """Shuffle list x in place, and return None."""
    for i in reversed(range(1, len(x))):
        # pick an element in x[:i+1] with which to exchange x[i]
        j = _rand_below(i + 1)
        x[i], x[j] = x[j], x[i]

cpdef xt_choices(population, weights=None, cum_weights=None, k=1):
    """Return a k sized list of population elements chosen with replacement.

    If the relative weights or cumulative weights are not specified,
    the selections are made with equal probability.

    """
    n = len(population)
    if cum_weights is None:
        if weights is None:
            floor = _floor
            n += 0.0    # convert to float for a small speed improvement
            return [population[floor(interf.xt_random() * n)] for i in _repeat(None, k)]
        try:
            cum_weights = list(_accumulate(weights))
        except TypeError:
            if not isinstance(weights, int):
                raise
            k = weights
            raise TypeError(f'The number of choices must be a keyword argument: {k}'.format(k=k)) from None
    elif weights is not None:
        raise TypeError('Cannot specify both weights and cumulative weights')
    if len(cum_weights) != n:
        raise ValueError('The number of weights does not match the population')
    total = cum_weights[-1] + 0.0   # convert to float
    if total <= 0.0:
        raise ValueError('Total of weights must be greater than zero')
    if not _isfinite(total):
        raise ValueError('Total of weights must be finite')
    bisect = _bisect
    hi = n - 1
    return [population[bisect(cum_weights, interf.xt_random()  * total, 0, hi)] for i in _repeat(None, k)]

cpdef xt_normalvariate(double mu=0.0, double sigma=1.0):
    """Normal distribution.

    mu is the mean, and sigma is the standard deviation.

    """
    # Uses Kinderman and Monahan method. Reference: Kinderman,
    # A.J. and Monahan, J.F., "Computer generation of random
    # variables using the ratio of uniform deviates", ACM Trans
    # Math Software, 3, (1977), pp257-260.
    cdef double u1, u2, z, zz
    while True:
        u1 = interf.xt_random()
        u2 = 1.0 - interf.xt_random()
        z = NV_MAGICCONST * (u1 - 0.5) / u2
        zz = z * z / 4.0
        if zz <= -_log(u2):
            break
    return mu + z * sigma

cpdef xt_lognormvariate(double mu, double sigma):
    """Log normal distribution.

    If you take the natural logarithm of this distribution, you'll get a
    normal distribution with mean mu and standard deviation sigma.
    mu can have any value, and sigma must be greater than zero.

    """
    return _exp(xt_normalvariate(mu, sigma))

cpdef xt_expovariate(double lambd):
    """Exponential distribution.

    lambd is 1.0 divided by the desired mean.  It should be
    nonzero.  (The parameter would be called "lambda", but that is
    a reserved word in Python.)  Returned values range from 0 to
    positive infinity if lambd is positive, and from negative
    infinity to 0 if lambd is negative.

    """
    # lambd: rate lambd = 1/mean
    # ('lambda' is a Python reserved word)

    # we use 1-random() instead of random() to preclude the
    # possibility of taking the log of zero.
    return -_log(1.0 - interf.xt_random()) / lambd


cpdef xt_vonmisesvariate(double mu, double kappa):
    """Circular data distribution.

    mu is the mean angle, expressed in radians between 0 and 2*pi, and
    kappa is the concentration parameter, which must be greater than or
    equal to zero.  If kappa is equal to zero, this distribution reduces
    to a uniform random angle over the range 0 to 2*pi.

    """
    # Based upon an algorithm published in: Fisher, N.I.,
    # "Statistical Analysis of Circular Data", Cambridge
    # University Press, 1993.

    # Thanks to Magnus Kessler for a correction to the
    # implementation of step 4.
    cdef double s, r, u1, z, d, u2, q, f, u3, theta
    if kappa <= 1e-6:
        return TWOPI * interf.xt_random()

    s = 0.5 / kappa
    r = s + _sqrt(1.0 + s * s)

    while True:
        u1 = interf.xt_random()
        z = _cos(_pi * u1)

        d = z / (r + z)
        u2 = interf.xt_random()
        if u2 < 1.0 - d * d or u2 <= (1.0 - d) * _exp(d):
            break

    q = 1.0 / r
    f = (q + z) / (1.0 + q * z)
    u3 = interf.xt_random()
    if u3 > 0.5:
        theta = (mu + _acos(f)) % TWOPI
    else:
        theta = (mu - _acos(f)) % TWOPI

    return theta

cpdef xt_gammavariate(double alpha, double beta):
    """Gamma distribution.  Not the gamma function!

    Conditions on the parameters are alpha > 0 and beta > 0.

    The probability distribution function is:

                x ** (alpha - 1) * math.exp(-x / beta)
      pdf(x) =  --------------------------------------
                  math.gamma(alpha) * beta ** alpha

    """
    # alpha > 0, beta > 0, mean is alpha*beta, variance is alpha*beta**2

    # Warning: a few older sources define the gamma distribution in terms
    # of alpha > -1.0
    cdef double ainv, bbb, ccc, u, u1, u2, v, z, r, b, p,
    if alpha <= 0.0 or beta <= 0.0:
        raise ValueError('gammavariate: alpha and beta must be > 0.0')
    if alpha > 1.0:
        # Uses R.C.H. Cheng, "The generation of Gamma
        # variables with non-integral shape parameters",
        # Applied Statistics, (1977), 26, No. 1, p71-74

        ainv = _sqrt(2.0 * alpha - 1.0)
        bbb = alpha - LOG4
        ccc = alpha + ainv

        while True:
            u1 = interf.xt_random()
            if not 1e-7 < u1 < 0.9999999:
                continue
            u2 = 1.0 - interf.xt_random()
            v = _log(u1 / (1.0 - u1)) / ainv
            x = alpha * _exp(v)
            z = u1 * u1 * u2
            r = bbb + ccc * v - x
            if r + SG_MAGICCONST - 4.5 * z >= 0.0 or r >= _log(z):
                return x * beta

    elif alpha == 1.0:
        # expovariate(1/beta)
        return -_log(1.0 - interf.xt_random()) * beta

    else:
        # alpha is between 0 and 1 (exclusive)
        # Uses ALGORITHM GS of Statistical Computing - Kennedy & Gentle
        while True:
            u = interf.xt_random()
            b = (_e + alpha) / _e
            p = b * u
            if p <= 1.0:
                x = p ** (1.0 / alpha)
            else:
                x = -_log((b - p) / alpha)
            u1 = interf.xt_random()
            if p > 1.0:
                if u1 <= (x ** (alpha - 1.0)):
                    break
            elif u1 <= _exp(-x):
                break
        return x * beta

cpdef xt_betavariate(double alpha, double beta):
    """Beta distribution.

    Conditions on the parameters are alpha > 0 and beta > 0.
    Returned values range between 0 and 1.

    """
    ## See
    ## http://mail.python.org/pipermail/python-bugs-list/2001-January/003752.html
    ## for Ivan Frohne's insightful analysis of why the original implementation:
    ##
    ##    def betavariate(self, alpha, beta):
    ##        # Discrete Event Simulation in C, pp 87-88.
    ##
    ##        y = self.expovariate(alpha)
    ##        z = self.expovariate(1.0/beta)
    ##        return z/(y+z)
    ##
    ## was dead wrong, and how it probably got that way.

    # This version due to Janne Sinkkonen, and matches all the std
    # texts (e.g., Knuth Vol 2 Ed 3 pg 134 "the beta distribution").
    cdef double y
    y = xt_gammavariate(alpha, 1.0)
    if y:
        return y / (y + xt_gammavariate(beta, 1.0))
    return 0.0

cpdef xt_paretovariate(double alpha):
    """Pareto distribution.  alpha is the shape parameter."""
    # Jain, pg. 495

    cdef double u = 1.0 - interf.xt_random()
    return u ** (-1.0 / alpha)

cpdef xt_weibullvariate(double alpha, double beta):
    """Weibull distribution.

    alpha is the scale parameter and beta is the shape parameter.

    """
    # Jain, pg. 499; bug fix courtesy Bill Arms

    cdef double u = 1.0 - interf.xt_random()
    return alpha * (-_log(u)) ** (1.0 / beta)

cpdef xt_seed(unsigned int seed):
    """
        change random seed with unsigned int
    """
    interf.reset_rand_seed(seed, 1)

cpdef xt_rand_init():
    """
    Initialize the random number generator
    This function initializes the random number generator state to ensure it is properly initialized only once before use.
    It checks the global variable XT_RAND_INIT to determine if initialization is needed.
    """
    global XT_RAND_INIT
    # Check if the random number generator has already been initialized
    if XT_RAND_INIT == 0:
        # If not initialized, call the underlying library's initialization function
        interf.init_rand(NULL, 1)
    # Set the state to initialized regardless of previous state to prevent re-initialization
    XT_RAND_INIT = 1


cpdef xt_gauss_init(unsigned long long mu, double sigma):
    """
    Initialize the Gaussian random number generator

    Parameters:
        mu: Mean of the Gaussian distribution
        sigma: Standard deviation of the Gaussian distribution
    
    Returns: None
    This function initializes the Gaussian random number generator to ensure it is only called once before generating random numbers
    """
    global XT_GAUSS_RAND_INIT
    # Check if the Gaussian random number generator needs initialization
    if XT_GAUSS_RAND_INIT == 0:
        # Call gauss_init function for initialization with mean and standard deviation as parameters
        interf.gauss_init(NULL, mu, sigma)
    # Mark that the Gaussian random number generator has been initialized
    XT_GAUSS_RAND_INIT = 1



cpdef xt_gauss(unsigned long long mu, double sigma):
    """
    Generates a random number following a Gaussian distribution with the specified mean and standard deviation.

    Parameters:
    - mu (unsigned long long): The mean of the Gaussian distribution.
    - sigma (double): The standard deviation of the Gaussian distribution.

    Returns:
    - double: A random number generated from the Gaussian distribution.
    """
    # Check if the Gaussian random number generator needs to be initialized
    if XT_GAUSS_RAND_INIT == 0:
        # If not initialized, call the initialization function
        xt_gauss_init(mu, sigma)
    else:
        # If already initialized, call the gauss_next method from the interf module to generate the next Gaussian random number
        return interf.gauss_next()

cpdef xt_lcg_init(unsigned long long start, unsigned long long stop, step=None, unsigned long long lcg_random=0, unsigned int reset_lcg=0):
    """
    Initialize the Linear Congruential Generator (LCG) with specified parameters.

    Parameters:
    - start: The starting value of the range.
    - stop: The ending value of the range.
    - step: The step size, which can be an integer, list, tuple, range object, or dictionary.
    - lcg_random: A pointer to the LCG random number generator.
    - reset_lcg: A flag indicating whether to reset the LCG.

    Returns:
    None
    """
    # Calculate the count of elements in the range
    cdef unsigned long long range_count = stop - start + 1
    cdef unsigned long long range_pow = 0
    cdef unsigned long long step_summary = 0
    cdef unsigned int _step = 0
    cdef unsigned int c_increment = 0
    cdef unsigned int *sub_step_arrays = NULL
    cdef unsigned int sub_step_count = 0
    cdef interf.xt_lcg_random * _lcg_random

    # Initialize _lcg_random based on the lcg_random parameter
    if lcg_random == 0:
        _lcg_random = NULL
    else:
        _lcg_random = <interf.xt_lcg_random *> lcg_random

    # Process the step parameter to calculate the total step summary and related parameters
    if type(step) is int:
        _step = step
        step_summary = step
    elif type(step) is list or type(step) is tuple or type(step) is range:
        sub_step_count = len(step)
        sub_step_arrays = <unsigned int *> malloc(sizeof(unsigned int) * sub_step_count)
        for index in range(len(step)):
            sub_step_arrays[index] = step[index]
            step_summary += step[index]
        _step = 1
    elif type(step) is dict:
        sub_step_count = sum(list(step.values()))
        sub_step_arrays = <unsigned int *> malloc(sizeof(unsigned int) * sub_step_count)
        sum_item = 0
        for key in step.keys():
            for index in range(step[key]):
                sub_step_arrays[sum_item] = key
                sum_item += 1
                step_summary += key
        _step = 1
    else:
        assert False, print("Received an invalid step value %s; expected types are int, list, tuple, range, or dict" % step)

    # Adjust the range count to be a multiple of the step summary
    range_count = range_count // step_summary
    # Calculate the next power of 2 greater than or equal to the adjusted range count
    range_pow = interf.roundup_pow2(range_count // step_summary)

    # Generate a new increment that is different from the current LCG increment
    while True:
        c_increment = xt_randint(1, range_count, 2)
        if _lcg_random.c_increment != c_increment:
            break
        else:
            print("lcg random: random c_increment %s and recover c_increment is the same" % c_increment)

    # Generate the initial random number x0 based on the type of step parameter
    if type(step) is int:
        x0 = xt_randint(start, stop, step)
    else:
        x0 = xt_randint(0, range_count, 1)

    # Reinitialize LCG selectively based on the range size and reset_lcg flag
    # 0x3ffffffed =  4294967291 * 4 + 1
    if range_pow < 13849:
        if reset_lcg and _lcg_random.a_multiplier != 5:
            if _lcg_random.a_multiplier + 4 > range_pow:
                interf.init_lcg_random(_lcg_random, x0=x0, m_modulus=range_pow, c_increment=1, a_multiplier=5, offset=start, max_value=stop, step=_step, sub_step_arrays=sub_step_arrays, sub_step_count=sub_step_count)
            else:
                interf.init_lcg_random(_lcg_random, x0=x0, m_modulus=range_pow, c_increment=1, a_multiplier=_lcg_random.a_multiplier + 4, offset=start, max_value=stop, step=_step, sub_step_arrays=sub_step_arrays, sub_step_count=sub_step_count)
        else:
            interf.init_lcg_random(_lcg_random, x0=x0, m_modulus=range_pow, c_increment=1, a_multiplier=5, offset=start, max_value=stop, step=_step, sub_step_arrays=sub_step_arrays, sub_step_count=sub_step_count)
    else:
        if reset_lcg and _lcg_random.a_multiplier != 5:
            if _lcg_random.a_multiplier + 2 > range_pow:
                interf.init_lcg_random(_lcg_random, x0=x0, m_modulus=range_pow, c_increment=c_increment, a_multiplier=0x3ffffffed, offset=start, max_value=stop, step=_step, sub_step_arrays=sub_step_arrays, sub_step_count=sub_step_count)
            else:
                interf.init_lcg_random(_lcg_random, x0=x0, m_modulus=range_pow, c_increment=1, a_multiplier=_lcg_random.a_multiplier + 4, offset=start, max_value=stop, step=_step, sub_step_arrays=sub_step_arrays, sub_step_count=sub_step_count)
        else:
            interf.init_lcg_random(_lcg_random, x0=x0, m_modulus=range_pow, c_increment=c_increment, a_multiplier=0x3ffffffed, offset=start, max_value=stop, step=_step, sub_step_arrays=sub_step_arrays, sub_step_count=sub_step_count)

    # Update the global LCG random state
    global g_xt_lcg_random
    g_xt_lcg_random = interf.get_lcg_random()


cpdef xt_lcg_first(unsigned long long start, unsigned long long stop, unsigned int step, unsigned long long lcg_random=0):
    """
    # Define a function `xt_lcg_first` that generates the first random number in a linear congruential sequence.
    This function allows the user to specify the range (start to stop) and step of the random number sequence.
    Parameters:
       start: The starting value of the random number sequence.
       stop: The ending value of the random number sequence.
       step: The step size of the random number sequence.
       lcg_random: A pointer to the state of the linear congruential generator, default is 0.
    Returns:
       The first random number in the linear congruential sequence.
    """
    # Define a pointer to the state of the linear congruential generator
    cdef interf.xt_lcg_random * _lcg_random

    # If no linear congruential generator state pointer is provided
    if lcg_random == 0:
        # Access the global linear congruential generator state
        global g_xt_lcg_random

        # If the global state is null, initialize the linear congruential generator
        if g_xt_lcg_random == NULL:
            xt_lcg_init(start, stop, step)

        # Use the global linear congruential generator state to generate and return the first random number
        return g_xt_lcg_random.next * step + g_xt_lcg_random.offset
    else:
        # If a linear congruential generator state pointer is provided, use the provided state
        _lcg_random = <interf.xt_lcg_random *> lcg_random

        # Use the provided linear congruential generator state to generate and return the first random number
        return _lcg_random.next * step + _lcg_random.offset


cpdef xt_lcg_next(unsigned long long lcg_random=0):
    """
    Generates the next random number based on the given random seed.

    Parameters:
    - lcg_random: An unsigned long long representing the random seed, default value is 0.
                  If 0, a new random seed will be initialized.

    Returns:
    - The result of generating the next random number.
    """
    cdef interf.xt_lcg_random * _lcg_random

    # Initialize the random seed pointer to NULL if lcg_random is 0
    if lcg_random == 0:
        _lcg_random = NULL
    else:
        # Convert lcg_random to a pointer of type interf.xt_lcg_random for further random number generation
        _lcg_random = <interf.xt_lcg_random *> lcg_random

    # Call lcg_next_start function with the random seed pointer to generate and return the next random number
    return interf.lcg_next_start(_lcg_random)


xt_rand_init()

