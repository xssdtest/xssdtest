#! /usr/bin/python3
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
import random

def value_power2_upward_align(value):
    """
    Aligns the given value upward to the nearest power of 2.

    If the given value is already a power of 2, it returns the value directly.
    If the given value is not a power of 2, it finds the smallest power of 2 greater than the value and returns it.

    Parameters:
    value (int): The integer to be aligned.

    Returns:
    int: The integer aligned to the nearest power of 2.
    """
    # Validate input
    if not isinstance(value, int) or value <= 0:
        raise ValueError("Input must be a positive integer.")

    # Check if value is already a power of 2
    if value & (value - 1) == 0:
        return value

    # Find the smallest power of 2 greater than value
    power = 1
    while power < value:
        power <<= 1

    return power

class Sub_LCG_Random(object):
    def __init__(self, sub_rang_list):
        self.sub_rang_list = sub_rang_list
        self.start = 0
        self.stop = len(self.sub_rang_list) - 1
        self.m_modulus = value_power2_upward_align(self.stop) - 1
        self.range_count = len(self.sub_rang_list)
        self.a_multiplier = random.randint(1, self.range_count // 4) * 4 + 1 if self.range_count // 4 > 5 else 5
        self.c_increment = random.randint(0, self.range_count // 2) * 2 + 1
        self.init_a_multiplier = self.a_multiplier
        self.init_c_increment = self.c_increment
        self.sub_next = self.start

    def sub_next_index(self):
        """
        Generate the next index value.

        This method uses a linear congruential generator (LCG) algorithm to generate the next index value.
        The LCG algorithm is a simple pseudo-random number generation algorithm that computes the next value
        from the current value, multiplier, increment, and modulus. This method is primarily used to generate
        pseudo-random and non-repeating index values in a series of operations until all possible index values
        have been used once.
        """
        # Use the linear congruential generator algorithm to calculate the next index value
        self.sub_next = (self.a_multiplier * self.sub_next + self.c_increment) & self.m_modulus

        # If the generated index value is greater than or equal to the stop value, recompute until a valid index value is obtained
        while self.sub_next > self.stop:
            self.sub_next = (self.a_multiplier * self.sub_next + self.c_increment) & self.m_modulus

        # Return the calculated next index value
        return self.sub_next

    def sub_lcg_reset(self, a_multiplier=None, c_increment=None):
        """
        Reset the parameters of the linear congruential generator.

        This function updates the multiplier and increment values based on the provided parameters or default rules.
        If no multiplier parameter is provided, the current multiplier is increased by 4 (unless adding 4 would exceed the modulus, in which case it is set to 5).
        Similarly, if no increment parameter is provided, the current increment is increased by 2 (unless adding 2 would exceed the modulus, in which case it is set to 1).

        :param a_multiplier: The new value to update the multiplier with. If not provided, it is updated based on the default rule.
        :param c_increment: The new value to update the increment with. If not provided, it is updated based on the default rule.
        """
        # Update the multiplier parameter, if no new value is provided, increase based on the default rule
        if a_multiplier is None:
            self.a_multiplier = self.a_multiplier + 4 if self.a_multiplier + 4 < self.m_modulus else 5
        else:
            self.a_multiplier = a_multiplier

        # Update the increment parameter, if no new value is provided, increase based on the default rule
        if c_increment is None:
            self.c_increment = self.c_increment + 2 if self.c_increment + 2 < self.m_modulus else 1
        else:
            self.c_increment = c_increment
    def sub_lcg_reinit(self):
        """
        Reinitialize the parameters of the Linear Congruential Generator (LCG).

        This method resets the multiplier and increment of the LCG to their initial values.
        """
        # Reset the multiplier to its initial value
        self.a_multiplier = self.init_a_multiplier
        # Reset the increment to its initial value
        self.c_increment = self.init_c_increment


class LCG_Random(object):
    def __init__(self, start=None, stop=None, step=None, x0=None, seed=None):
        self.offset = start if start is not None else 0
        self.sub_range = self.init_sub_range(step)
        stop = 0xFFFFFFFFFFFFFFFF if stop is None else stop
        self.__range = (stop - start + 1) // self.sub_range
        self.m_modulus = value_power2_upward_align(self.__range) - 1
        self.range_count = self.get_range_count(start=start, stop=stop, step=step)
        self.sub_count = self.range_count // len(self.sub_rang_list) * len(self.sub_rang_list)
        self.count = 0
        if seed is None:
            random.seed(seed)
        self.a_multiplier = random.randint(1, self.range_count // 4) * 4 + 1 if self.range_count // 4 > 5 else 5
        self.c_increment = random.randint(0, self.range_count // 2) * 2 + 1
        self.next = x0 if x0 is not None else start
        self.sub_range_count = 0
        self.sub_next = -1
        self.sub_summary = 0
        if len(self.sub_rang_list) > 1:
            self.sub_lcg = Sub_LCG_Random(self.sub_rang_list)
            self.sub_lcg_count = len(self.sub_rang_list)
    def get_range_count(self, start=None, stop=None, step=None):
        """
        Calculate the number of sub-ranges within the given range and step.

        :param start: The start value of the range. If None, the start is not considered.
        :param stop: The end value of the range. If None, the end is not considered.
        :param step: The step value. If None or an integer, it defaults to 1.
        :return: The number of sub-ranges contained within the specified range.
        """
        # Directly calculate the number of sub-ranges if step is None or an integer
        if step is None or isinstance(step, int):
            return (stop - start + 1) // self.sub_range
        else:
            # Calculate the offset to ensure accurate range calculation
            _offset = (stop - start + 1) // self.sub_range * self.sub_range + start
            # Initialize the sub-range counter
            _count = (stop - start + 1) // self.sub_range * len(self.sub_rang_list)
            # Iterate over the sub-range list and adjust the offset and counter based on each sub-range step
            for _step in self.sub_rang_list:
                _offset += _step
                # Increase the counter if the adjusted offset is still within the specified range
                if _offset - 1 <= stop:
                    _count += 1
                else:
                    # Stop calculation if the offset exceeds the range
                    break
            # Return the final count of sub-ranges
            return _count

    def init_sub_range(self, step):
        """
        Initialize the sub-range based on the provided step parameter.

        This function calculates the total sub-range and updates the sub-range list 
        according to the type of the step parameter (integer, list, or dictionary).

        Parameters:
        - step: Can be an integer, list, or dictionary representing the step or combination of steps.

        Returns:
        None. This function updates the instance attributes `sub_range` and `sub_rang_list`.
        """
        # Initialize sub_range to 0 and sub_rang_list to an empty list
        sub_range = 0
        self.sub_rang_list = []

        # Handle the case where step is None or an integer
        if step is None or isinstance(step, int):
            # Set sub_range to step if it's not None; otherwise, default to 1
            sub_range = step if step is not None else 1
            # Append the sub_range to the sub_rang_list
            self.sub_rang_list.append(sub_range)
        
        # Handle the case where step is a non-empty list
        elif isinstance(step, list) and step:
            # Calculate the sum of all elements in the list as the sub_range
            sub_range = sum(step)
            # Assign the list to sub_rang_list
            self.sub_rang_list = step
        
        # Handle the case where step is a non-empty dictionary
        elif isinstance(step, dict) and step:
            # Iterate over each key-value pair in the dictionary
            for key, value in step.items():
                # Ensure both key and value are integers
                if not isinstance(key, int):
                    raise ValueError(f"Invalid key type: {type(key)}, expected int")
                if not isinstance(value, int):
                    raise ValueError(f"Invalid value type: {type(value)}, expected int")
                # Calculate the sub_range based on key-value pairs
                sub_range += key * value
                # Extend the sub_rang_list with repeated keys
                self.sub_rang_list += [key] * value
        
        # Raise an error if step is of an invalid type
        else:
            raise ValueError(f"Invalid step type: {type(step)}")

        return sub_range

    def next_start(self):
        """
        Generate the next starting point.

        This function determines the next starting point based on whether the current instance has a `sub_lcg` attribute.
        If `sub_lcg` is not present, it generates the next starting point by iterating within the defined range until an unused point is found.
        If `sub_lcg` is present, it follows the rules defined by `sub_lcg` to generate the next starting point.

        Returns:
            int: The next starting point calculated based on the specified algorithm.
        """
        if not hasattr(self, 'sub_lcg'):
            # No sub_lcg attribute; iterate to find the next unused starting point within the range.
            self.next = (self.a_multiplier * self.next + self.c_increment) & self.m_modulus
            while self.next >= self.__range:
                self.next = (self.a_multiplier * self.next + self.c_increment) & self.m_modulus
            return self.next * self.sub_range + self.offset
        else:
            # sub_lcg attribute is present; follow its rules to generate the next starting point.
            if self.sub_next == -1:
                # sub_next is -1, indicating the need to find a new unused starting point within the current range.
                self.sub_summary = 0
                self.next = (self.a_multiplier * self.next + self.c_increment) & self.m_modulus
                while self.next >= self.__range:
                    self.next = (self.a_multiplier * self.next + self.c_increment) & self.m_modulus
                self.sub_next = self.sub_lcg.sub_next_index()
            else:
                # sub_next is already set, use the existing value.
                self.sub_next = self.sub_lcg.sub_next_index()
                self.sub_summary += self.sub_rang_list[self.sub_next]

            self.count += 1
            self.sub_range_count += 1

            # Check if all sub_lcg starting points have been used; reset sub_lcg if necessary.
            if self.sub_range_count == self.sub_lcg_count:
                self.sub_next = -1
                self.sub_range_count = 0
                self.sub_lcg.sub_lcg_reset()
            return self.next * self.sub_range + self.sub_summary + self.offset

    def lcg_list(self):
        # Initialize counter
        count = 0

        if hasattr(self, 'sub_lcg'):
            self.sub_lcg.sub_lcg_reinit()

        # Generate the first sub_count numbers
        while count < self.sub_count:
            yield self.next_start()
            count += 1

        # Calculate the edge value for subsequent number generation
        sub_edge = self.offset + self.sub_range * self.__range - 1

        self.sub_summary = 0

        while count < self.range_count:
            self.sub_summary += self.sub_rang_list[self.sub_count - count]
            yield sub_edge + self.sub_summary
            count += 1

    def reset_lcg_list(self, a_multiplier=None, c_increment=None):
        """
        Resets the parameters of the Linear Congruential Generator (LCG).

        If new multipliers and increments are not provided, it automatically adjusts
        the current parameters based on the modulus to maintain the randomness properties
        of the LCG.

        Parameters:
        - a_multiplier (int, optional): New multiplier. If not provided, it is automatically adjusted based on the current multiplier and modulus.
        - c_increment (int, optional): New increment. If not provided, it is automatically adjusted based on the current increment and modulus.
        """
        # Automatically adjust or set the multiplier
        if a_multiplier is None:
            self.a_multiplier = self.a_multiplier + 4 if self.a_multiplier + 4 < self.m_modulus else 5
        else:
            self.a_multiplier = a_multiplier

        # Automatically adjust or set the increment
        if c_increment is None:
            self.c_increment = self.c_increment + 2 if self.c_increment + 2 < self.m_modulus else 1
        else:
            self.c_increment = c_increment

        self.count = 0
        self.sub_next = -1

if __name__=="__main__":
    lcg = LCG_Random(start=0, step=2, stop=0x10)
    lcg_list = list(lcg.lcg_list())
    print(lcg_list)
    print(len(lcg_list))

    lcg = LCG_Random(start=0, step=[1, 2, 3, 4], stop=100)
    lcg_list = list(lcg.lcg_list())
    print(lcg_list)
    print(len(lcg_list))