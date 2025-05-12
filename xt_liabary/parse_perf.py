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
import os
import datetime
import uuid
import math
import pyecharts.options as opts
from pyecharts.charts import Line, Grid
from typing import List, Union
def _sum_fio_index_io(io_data, offset, job_number):
    """
    Calculate the sum of values at the specified offset position in each element of the io_data list, ignoring None values or positions beyond the list length.

    Parameters:
    - io_data: A list containing multiple data lists.
    - offset: The specified offset position.
    - job_number: The number of data lists to process.

    Returns:
    - The sum of valid data. If all data is considered invalid, returns 0.
    - Raises an exception if the input parameters are invalid (e.g., io_data is empty or job_number is non-positive).
    """
    # Validate input parameters
    if not io_data or job_number <= 0:
        raise ValueError("io_data cannot be empty, and job_number must be a positive number.")

    # Initialize sum and invalid data counter
    sum_value, invalid_data_count = 0, 0

    # Iterate through each data list
    for index in range(job_number):
        # Check if the current position is valid
        if offset >= len(io_data[index]) or io_data[index][offset] is None:
            invalid_data_count += 1
            continue
        # Accumulate valid data values
        sum_value += io_data[index][offset]

    # Return 0 if all data is considered invalid
    if invalid_data_count == job_number:
        return 0

    # Return the sum of valid data
    return sum_value


def _fio_bound_calculate(value, unit):
    """
    Calculate a boundary value that meets specific constraints based on the given value and unit.

    Parameters:
    value (int): The original value for which the boundary needs to be calculated.
    unit (int): The unit used to determine the boundary condition.

    Returns:
    int: The calculated boundary value.

    Raises:
    ValueError: If the unit is not a positive number, this exception is raised.

    Description:
    The purpose of this function is to ensure that the returned value is an integer multiple of the unit.
    If the remainder is between one-quarter and three-quarters of the unit, it adjusts the value to be closer to the next unit.
    """
    # Ensure the unit is a positive number; otherwise, raise an assertion error
    assert unit > 0, print("Unit must be a positive number.")

    # Calculate the remainder when dividing the value by the unit
    _mod = value % unit

    # If the remainder is 0, the value is already a multiple of the unit, so return it directly
    if _mod == 0:
        return value
    else:
        # If the remainder is less than one-quarter of the unit, round down to the nearest multiple of the unit
        if _mod < unit // 4:
            return value // unit * unit

        # If the remainder is greater than three-quarters of the unit, adjust to the next multiple of the unit
        elif _mod > unit // 4 * 3:
            return value - _mod + unit

        # If the remainder is between one-quarter and three-quarters of the unit, it theoretically should not occur; handle with an assertion
        else:
            assert False, print("get an invalid bound value:%s unit:%s" % (value, unit))


def _sum_fio_rw_data(read_value, write_value):
    """
    Calculate the sum of read and write data, prioritizing non-None values.

    If both read and write values are None, return their sum (which will be None).
    If only the read value is None, return the write value.
    If only the write value is None, return the read value.

    :param read_value: The amount of data for the read operation.
    :param write_value: The amount of data for the write operation.
    :return: The total sum of read and write operation data.
    """
    if read_value is None:
        return write_value
    else:
        return read_value if write_value is None else read_value + write_value



def _get_list_max_value(lst: List[Union[int, float]]) -> Union[int, float]:
    """
    Finds the largest value from the given list.

    Parameters:
    lst (List[Union[int, float]]): A list containing integers or floating-point numbers.

    Returns:
    Union[int, float]: The maximum value in the list. If the list is empty, returns 0.
    """
    # Uses the built-in max function to simplify logic and improve efficiency
    return max(filter(None, lst), default=0)



def _get_list_min_value(lst: List[Union[int, float]]) -> Union[int, float]:
    """
    Get the minimum value in the list.
    Parameters:
        lst (List[Union[int, float]]): A list containing integers or floating-point numbers.
    Returns:
        Union[int, float]: The minimum value in the list. If the list is empty, return 0.
    Note:
        - If the list contains `None`, this function treats it as infinity and returns the smallest numeric value in the list or 0 if the list is empty.
        - If the list contains incomparable types, this function will raise a `TypeError`.
    """
    # Initialize the minimum value as the first element of the list, or 0 if the list is empty
    minimum_value = lst[0] if len(lst) else 0

    # Iterate through the list to find the minimum value, skipping `None`
    for value in lst:
        if value is not None and value < minimum_value:
            minimum_value = value

    # Return the final minimum value
    return minimum_value



def _get_list_statistics(lst):
    """
    Calculate the sum, minimum, maximum, and average of all non-None elements in a list.

    Parameters:
        lst (list): A list containing numerical values.

    Returns:
        tuple: A tuple containing the minimum, maximum, and average values.
    """
    if not lst:  # Check if the list is empty
        return None, None, None  # Return None to indicate no data

    total_sum, count, min_val, max_val = 0, 0, float('inf'), float('-inf')
    for value in lst:
        if value is None or not isinstance(value, (int, float)):  # Check if the element is None or a numerical type
            continue
        total_sum += value
        count += 1
        min_val = min(min_val, value)
        max_val = max(max_val, value)

    average = total_sum / count  # Use floating-point division to retain decimal places
    return min_val, max_val, int(average)  # Return the integer average to maintain functionality and internal consistency



def _parse_fio_file(parse_files, delimiter, xaxis_unit):
    """
    Parses FIO test result files, extracts IO data, and performs aggregation calculations.

    Parameters:
    parse_files (str): Path to the FIO test result file to be parsed.
    delimiter (str): Delimiter between data fields in the file.
    xaxis_unit (str): Unit for the x-axis data.

    Returns:
    tuple: A tuple containing the following elements:
        - xaxis_data (list): List of x-axis data points.
        - write_data (list): List of write IO data in chronological order.
        - read_data (list): List of read IO data in chronological order.
        - totalio_data (list): List of total read/write IO data in chronological order.
        - total_read_data (list): List of total read IO data in chronological order.
        - total_write_data (list): List of total write IO data in chronological order.
    """
    io_data, write_data, read_data, xaxis_data, lines, index_check = [], [], [], [], [], 0

    # Check if the file path is valid
    assert os.path.exists(parse_files), print("get a invalid file path: %s" % parse_files)

    with open(parse_files, "r") as f:
        for _line in f:
            line_cont = _line.split(delimiter)
            key = _fio_bound_calculate(int(line_cont[0], 0), xaxis_unit)
            value, io_type = int(line_cont[1], 0), float(line_cont[2])

            # Initialize or extend data arrays to ensure read/write data lengths match
            if not xaxis_data or xaxis_data[0] == key:
                if len(write_data) == 0 or len(write_data[-1]) == len(read_data[-1]):
                    index_check = -1
                    write_data.append([]), read_data.append([])
                if not xaxis_data:
                    xaxis_data.append(key)

            # Ensure xaxis_data grows in order
            if xaxis_data[-1] < key:
                xaxis_data.append(key)

            # Update index check value to ensure data is correctly mapped to xaxis_data
            index_check = index_check + 1 if xaxis_data.index(key) != index_check else index_check

            # Depending on IO type, add data to either read or write data arrays
            if io_type == 0:
                read_data[-1] = read_data[-1] + [value] if xaxis_data[index_check] == key else read_data[-1] + [
                    None] * (xaxis_data.index(key) - index_check)
            else:
                write_data[-1] = write_data[-1] + [value] if xaxis_data[index_check] == key else write_data[-1] + [
                    None] * (xaxis_data.index(key) - index_check)

            # Update index check value to handle data jumps or repeats
            index_check = index_check + 1 if xaxis_data[-1] < key else index_check if xaxis_data[
                                                                                          index_check] == key else index_check + 1

        # Aggregate IO data across all jobs
        if write_data and read_data:
            for _index in range(len(read_data)):
                io_data.append([])
                for _off in range(len(read_data[_index])):
                    io_data[_index].append(_sum_fio_rw_data(read_data[_index][_off], write_data[_index][_off]))

    # Calculate total IO data for each time point
    totalio_data, total_read_data, total_write_data, job_number = [], [], [], len(io_data)
    for offset in range(len(xaxis_data)):
        if write_data:
            total_write_data.append(_sum_fio_index_io(write_data, offset, job_number))
        if read_data:
            total_read_data.append(_sum_fio_index_io(read_data, offset, job_number))
        if read_data and write_data:
            totalio_data.append(_sum_fio_index_io(io_data, offset, job_number))

    return xaxis_data, write_data, read_data, totalio_data, total_read_data, total_write_data


def _fio_summary_line_chart(totalio_data, total_read_data, total_write_data, xaxis_data, chart_title, yaxis_name,
                            expect_value, set_min_value, min_line, max_line, average_line):
    """
    Draws a line chart summarizing FIO performance test results.

    Parameters:
    totalio_data: List of total IO data.
    total_read_data: List of total read data.
    total_write_data: List of total write data.
    xaxis_data: List of data for the X-axis.
    chart_title: Title of the chart.
    yaxis_name: Name of the Y-axis.
    expect_value: Expected value to be marked on the chart.
    set_min_value: Whether to set the minimum value for the Y-axis.
    min_line: Whether to display the minimum value line.
    max_line: Whether to display the maximum value line.
    average_line: Whether to display the average value line.

    Returns:
    Line object representing the drawn line chart.
    """
    # Initialize the line chart object
    line1 = Line(init_opts=opts.InitOpts(width="100%"))
    # Add X-axis data
    line1.add_xaxis(xaxis_data=xaxis_data)
    # Initialize mark data for displaying special values on the chart
    _mark_data = [] if expect_value is None else [
        opts.MarkLineItem(name='expect value', y=expect_value, linestyle_opts=opts.LineStyleOpts(color="green"),
                          type_="dotted")]

    # Process statistics and mark data based on the presence of read and write data
    if total_read_data and total_write_data:
        _min, _max, _average = _get_list_statistics(totalio_data)
        series_name, y_axis = "iomix", totalio_data
        # Add read and write data to the chart
        line1.add_yaxis(series_name="readmix", y_axis=total_read_data, symbol_size=0)
        line1.add_yaxis(series_name="writemix", y_axis=total_write_data, symbol_size=0)
        max_value = int(_max * 1.2)
        _min_value = min(_get_list_min_value(total_read_data), _get_list_min_value(total_write_data))
    else:
        if total_read_data:
            _min, _max, _average = _get_list_statistics(total_read_data)
            series_name, y_axis = "readmix", total_read_data
            max_value, _min_value = int(_max * 1.2), _min
            _min_value = _get_list_min_value(total_read_data)
        else:
            _min, _max, _average = _get_list_statistics(total_write_data)
            series_name, y_axis = "writemix", total_write_data
            assert total_write_data, print("get a invalid total_write_data")
            max_value, _min_value = int(_max * 1.2), _min

    # Add minimum, maximum, and average value mark data based on parameters
    if min_line:
        _mark_data.append(opts.MarkLineItem(name='min value', y=_min, linestyle_opts=opts.LineStyleOpts(color="red")))
    if max_line:
        _mark_data.append(opts.MarkLineItem(name='max value', y=_max, linestyle_opts=opts.LineStyleOpts(color="red")))
    if average_line:
        _mark_data.append(
            opts.MarkLineItem(name='average value', y=_average, linestyle_opts=opts.LineStyleOpts(color="black")))

    # Add data series to the chart and set mark lines
    line1.add_yaxis(series_name=series_name, y_axis=y_axis, symbol_size=0,
                    markline_opts=opts.MarkLineOpts(data=_mark_data, symbol=None, symbol_size=0))

    # Adjust the maximum value of the Y-axis based on the data range
    max_value = max_value if int(math.log10(max_value * 0.1)) <= 1 else max_value - (
                max_value % (10 ** int(math.log10(max_value * 0.1))))

    # Set the minimum value of the Y-axis based on parameters
    if set_min_value:
        min_value = 0 if int(math.log10(max_value * 0.1)) <= 1 else _min_value - (
                    _min_value % (10 ** int(math.log10(max_value * 0.1))))
        min_value = 0 if min_value < 0 else min_value
    else:
        min_value = 0

    # Set various global options for the chart, such as title, tooltip, axis configuration, etc.
    line1.set_global_opts(
        title_opts=opts.TitleOpts(title=chart_title, pos_left="center"),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        axispointer_opts=opts.AxisPointerOpts(is_show=True, link=[{"xAxisIndex": "none"}]),
        datazoom_opts=[opts.DataZoomOpts(is_show=True, type_="inside", is_realtime=True, range_start=0, range_end=100,
                                         xaxis_index=[0, 1], )],
        xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False,
                                 axisline_opts=opts.AxisLineOpts(is_on_zero=False, ), ),
        yaxis_opts=opts.AxisOpts(type_="value", max_=max_value, min_=min_value, name=yaxis_name, name_gap=15),
        legend_opts=opts.LegendOpts(type_="scroll", selected_mode="multiple", selector=True, pos_top="top",
                                    pos_left="left"),
        toolbox_opts=opts.ToolboxOpts(is_show=True, pos_left="80%"),
    )
    # Hide data labels
    line1.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    return line1

def _fio_subline_chart(io_data, _type, xaxis_data, set_min_value):
    """
    Generate a sub-line chart based on the input data.

    Parameters:
    io_data: List of read/write data for each task.
    _type: Task type identifier, 0 for read, 1 for write.
    xaxis_data: List of data to be displayed on the x-axis.
    set_min_value: Whether to set a minimum value to control the minimum scale of the y-axis.

    Returns:
    line1: The generated sub-line chart object.
    """
    # Assert that io_data and xaxis_data are not empty
    assert io_data or xaxis_data, "io_data and xaxis_data cannot be empty."

    # Initialize the line chart object
    line1 = Line(init_opts=opts.InitOpts(width="100%"))
    # Add x-axis data
    line1.add_xaxis(xaxis_data=xaxis_data)

    # Initialize max and min values
    max_value, min_value = 0, 0

    # Iterate through io_data to generate lines for each task
    for index, _io_data in enumerate(io_data):
        # Generate series name based on task type
        series_name = "job%sread" % (index + 1) if _type == 0 else "job%swrite" % (index + 1)
        # Add y-axis data with symbol size set to 0
        line1.add_yaxis(series_name=series_name, y_axis=_io_data, symbol_size=0)
        # Get the max and min values of the current task data
        _max_value = _get_list_max_value(_io_data)
        _min_value = _get_list_min_value(_io_data)
        # Update global max and min values
        min_value = _min_value if _min_value < min_value else min_value
        max_value = max_value if _max_value < max_value else _max_value

    # Calculate the max value, considering visual aesthetics, scale it up appropriately
    max_value = int(max_value * 1.2)
    # Adjust the max value to make it appear neat on the scale
    max_value = max_value if int(math.log10(max_value * 0.1)) <= 2 else max_value - (
                max_value % 10 ** int(math.log10(max_value * 0.1)))

    # If set_min_value is True, adjust the min value based on the max value
    if set_min_value:
        min_value = 0 if int(math.log10(max_value * 0.1)) <= 1 else _min_value - (
                    _min_value % (10 ** int(math.log10(max_value * 0.1))))
        # Ensure the min value is not negative
        min_value = 0 if min_value < 0 else min_value
    else:
        # If set_min_value is False, default to 0
        min_value = 0

    # Set global options including y-axis, x-axis, and legend
    line1.set_global_opts(
        yaxis_opts=opts.AxisOpts(type_="value", max_=max_value, min_=min_value, is_show=True),
        xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False, is_show=False, axisline_opts=opts.AxisLineOpts(is_on_zero=False, )),
        legend_opts=opts.LegendOpts(type_="scroll", selected_mode="multiple", pos_bottom="bottom", pos_left="left"),
    )
    # Hide data labels
    line1.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    # Return the generated line chart object
    return line1



def _set_local_javascript(path):
    """
    Replace JavaScript resource links in the specified file with local paths.

    This function reads the content of the file at the given path, extracts JavaScript resource links (containing 'https'),
    and replaces them with corresponding local filenames to achieve resource localization.

    Parameters:
    - path: The file path to be processed.

    Exceptions:
    - AssertionError: If the specified file path does not exist, an assertion error is raised.
    """
    # Ensure the file path exists
    assert os.path.exists(path), "path %s does not exist." % path

    # Initialize an empty list to store the processed file content
    lines = []

    # Open the file, read and process each line
    with open(path, "r") as f:
        for line in f:
            # Check if the current line contains 'javascript'
            if 'javascript' in line:
                # Split the line content by double quotes to extract JavaScript resource links
                _conts = line.split('"')
                # For each item, if it contains 'https', extract the last part as the local filename
                line = '"'.join([item if 'https' not in item else item.split("/")[-1] for item in _conts])
            # Append the processed line to the lines list
            lines.append(line)

    # Reopen the file and write the processed content back
    with open(path, "w") as f:
        f.writelines(lines)


def export_fio_line_chart(parse_files, delimiter, base_date, date_format, xaxis_unit, chart_title, yaxis_name,
                          show_all_lines,
                          output_path, expect_value, set_min_value, min_line, max_line, average_line, local_js):
    """
    Export a line chart for FIO performance test results.

    :param parse_files: List of FIO test result files to be parsed.
    :param delimiter: Delimiter used in the files.
    :param base_date: Base date for converting x-axis data to specific dates.
    :param date_format: Format of the base date.
    :param xaxis_unit: Time unit for the x-axis.
    :param chart_title: Title of the line chart.
    :param yaxis_name: Name of the y-axis.
    :param show_all_lines: Whether to display all sub-line charts.
    :param output_path: Output path for the chart.
    :param expect_value: Expected performance value.
    :param set_min_value: Whether to set the minimum value for the y-axis.
    :param min_line: Whether to display the minimum performance line.
    :param max_line: Whether to display the maximum performance line.
    :param average_line: Whether to display the average performance line.
    :param local_js: Whether to use local JavaScript files.
    """
    # Initialize the list of lines
    lines = []

    # Parse FIO files to get x-axis data and read/write performance data
    xaxis_data, write_data, read_data, totalio_data, total_read_data, total_write_data = _parse_fio_file(parse_files,
                                                                                                         delimiter,
                                                                                                         xaxis_unit)

    # If a base date is specified, convert x-axis data to specific dates
    if base_date:
        assert xaxis_unit >= 1000, "The minimum x-axis unit is 1000 milliseconds, input is %s" % xaxis_unit
        base_data = datetime.datetime.strptime(base_date, date_format)
        xaxis_data = [str(base_data + datetime.timedelta(milliseconds=x)) for x in xaxis_data]
    else:
        xaxis_data = ["%s" % (item // xaxis_unit) for item in xaxis_data]

    # Add the overall performance line to the list of lines
    lines.append(
        _fio_summary_line_chart(totalio_data, total_read_data, total_write_data, xaxis_data, chart_title, yaxis_name,
                                expect_value, set_min_value, min_line, max_line, average_line))

    # If there is more than one read data line, add the read performance sub-line to the list
    if len(read_data) > 1:
        lines.append(_fio_subline_chart(read_data, 0, xaxis_data, set_min_value))

    # If there is more than one write data line, add the write performance sub-line to the list
    if len(write_data) > 1:
        lines.append(_fio_subline_chart(write_data, 1, xaxis_data, set_min_value))

    # If an output path is specified, generate the final output path
    if output_path:
        if not output_path.endswith(".html"):
            output_path = output_path + "-%s_%s.html" % (
            datetime.datetime.now().strftime(r"%Y-%m-%d_%H:%M:%S"), uuid.uuid4().hex)
    else:
        output_path = "xt_line-%s_%s.html" % (datetime.datetime.now().strftime(r"%Y-%m-%d_%H:%M:%S"), uuid.uuid4().hex)

    # Render the chart based on the number of lines and whether to show all lines
    if len(lines) == 1 or not show_all_lines:
        lines[0].render(output_path)
    else:
        grid = Grid(init_opts=opts.InitOpts(width="100%"))
        grid.add(chart=lines[0], grid_opts=opts.GridOpts(height="50%"))
        l1 = lines[1]
        for _l1 in lines[2:]:
            l1 = l1.overlap(_l1)
        grid.add(chart=l1, grid_opts=opts.GridOpts(pos_top="70%", height="15%"))
        grid.render(output_path)

    # If using local JavaScript files, set up local JavaScript
    if local_js:
        _set_local_javascript(output_path)



def export_multfio_lines_chart(parse_files, delimiter, xaxis_unit, chart_title, yaxis_name, output_path, local_js):
    """
    Exports a line chart for multi-threaded FIO performance data.

    :param parse_files: List of FIO test result files to be parsed.
    :param delimiter: Delimiter used for file parsing.
    :param xaxis_unit: Unit for the x-axis.
    :param chart_title: Title of the line chart.
    :param yaxis_name: Name of the y-axis.
    :param output_path: Output path for the chart. If not specified, a unique path will be generated automatically.
    :param local_js: Whether to use local JavaScript files.
    """
    # Initialize data lists and maximum value
    lines_data, max_value, xaxis_data = [], None, []

    # Iterate through the file list, parse data, and populate the chart data structure
    for _path in parse_files:
        _xaxis_data, _, _, totalio_data, _, _ = _parse_fio_file(parse_files, delimiter, xaxis_unit)
        # Select the longest x-axis dataset
        xaxis_data = xaxis_data if len(xaxis_data) > len(_xaxis_data) else _xaxis_data
        series_name = os.path.basename(_path).split("-")[0]
        lines_data.append([series_name, totalio_data])

    # Initialize the line chart instance
    line1 = Line(init_opts=opts.InitOpts(width="100%"))

    # Set x-axis data
    line1.add_xaxis(xaxis_data=xaxis_data)

    # Iterate through each data set, add it to the line chart, and update the maximum value
    for _lineData in lines_data:
        line1.add_yaxis(series_name=_lineData[0], y_axis=_lineData[1], symbol_size=0)
        _max_value = int(_get_list_max_value(_lineData[1]) * 1.2)
        max_value = _max_value if max_value is None or _max_value > max_value else max_value

    # Adjust the maximum value of the y-axis based on the data range
    max_value = max_value if int(math.log10(max_value * 0.1)) <= 2 else max_value - (
                max_value % 10 ** int(math.log10(max_value * 0.1)))

    # Set various global options for the chart
    line1.set_global_opts(
        title_opts=opts.TitleOpts(title=chart_title, pos_left="center"),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        axispointer_opts=opts.AxisPointerOpts(is_show=True, link=[{"xAxisIndex": "none"}]),
        datazoom_opts=[opts.DataZoomOpts(is_show=True, type_="inside", is_realtime=True, range_start=0, range_end=100,
                                         xaxis_index=[0, 1], )],
        xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False,
                                 axisline_opts=opts.AxisLineOpts(is_on_zero=False, ), ),
        yaxis_opts=opts.AxisOpts(type_="value", max_=max_value, name=yaxis_name, name_gap=15),
        legend_opts=opts.LegendOpts(type_="scroll", selected_mode="multiple", pos_bottom="bottom", pos_left="left"),
        toolbox_opts=opts.ToolboxOpts(is_show=True, pos_left="80%"),
    )

    # Hide data labels
    line1.set_series_opts(label_opts=opts.LabelOpts(is_show=False))

    # Generate the final output path if not specified
    if output_path:
        if not output_path.endswith(".html"):
            output_path = output_path + "-%s_%s.html" % (
            datetime.datetime.now().strftime(r"%Y-%m-%d_%H:%M:%S"), uuid.uuid4().hex)
    else:
        output_path = "xt_line-%s_%s.html" % (datetime.datetime.now().strftime(r"%Y-%m-%d_%H:%M:%S"), uuid.uuid4().hex)

    # Render and save the chart
    line1.render(output_path)

    # Set local JavaScript if specified
    if local_js:
        _set_local_javascript(output_path)
