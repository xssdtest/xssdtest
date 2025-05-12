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
import zlib
bit_patterns = ['00000000-1', 'FFFFFFFF-2']
byte_patterns = ['12121212-3', '34343434-4', '56565656-5', '78787878-6', '90909090-7']
word_patterns = ['12341234-8', '23452345-9', '45674567-10', '56785678-11', '67896789-12', '789A789A-13', '89AB89AB-14', '9ABC9ABC-15', 'ABCDABCD-16', 'BCDEBCDE-17', 'CDEFCDEF-18', 'DEF0DEF0-19']
dword_patterns = ['12345678-20', '23456789-21', '3456789A-22', '456789AB-23', '56789ABC-24', '6789ABCD-25', '789ABCDE-26', '89ABCDEF-27', '9ABCDEF0-28', 'ABCDEF01-29', 'BCDEF012-30', 'CDEF0123-31']
incompressible_patterns = ['incompressible_data-32', 'incompressible_data-33', 'incompressible_data-34', 'incompressible_data-35', 'incompressible_data-36', 'incompressible_data-37', 'incompressible_data-38', 'incompressible_data-39', 'incompressible_data-40', 'incompressible_data-41',
                           'incompressible_data-42', 'incompressible_data-43', 'incompressible_data-44', 'incompressible_data-45', 'incompressible_data-46', 'incompressible_data-47', 'incompressible_data-48', 'incompressible_data-49', 'incompressible_data-50', 'incompressible_data-51',
                           'incompressible_data-52', 'incompressible_data-53', 'incompressible_data-54', 'incompressible_data-55', 'incompressible_data-56', 'incompressible_data-57', 'incompressible_data-58', 'incompressible_data-59', 'incompressible_data-60', 'incompressible_data-61',
                           'incompressible_data-62', 'incompressible_data-63', 'incompressible_data-64', 'incompressible_data-65', 'incompressible_data-66', 'incompressible_data-67', 'incompressible_data-68', 'incompressible_data-69', 'incompressible_data-70', 'incompressible_data-71',
                           'incompressible_data-72', 'incompressible_data-73', 'incompressible_data-74', 'incompressible_data-75', 'incompressible_data-76', 'incompressible_data-77', 'incompressible_data-78', 'incompressible_data-79', 'incompressible_data-80', 'incompressible_data-81',
                           'incompressible_data-82', 'incompressible_data-83', 'incompressible_data-84', 'incompressible_data-85', 'incompressible_data-86', 'incompressible_data-87','incompressible_data-88', 'incompressible_data-89', 'incompressible_data-90', 'incompressible_data-91']
double_compressible_patterns = ['2x_compressible_data-92', '2x_compressible_data-93', '2x_compressible_data-94', '2x_compressible_data-95', '2x_compressible_data-96', '2x_compressible_data-97', '2x_compressible_data-98', '2x_compressible_data-99', '2x_compressible_data-100', '2x_compressible_data-101',
                                '2x_compressible_data-102', '2x_compressible_data-103', '2x_compressible_data-104', '2x_compressible_data-105', '2x_compressible_data-106', '2x_compressible_data-107', '2x_compressible_data-108', '2x_compressible_data-109', '2x_compressible_data-110', '2x_compressible_data-111',
                                '2x_compressible_data-112', '2x_compressible_data-113', '2x_compressible_data-114', '2x_compressible_data-115', '2x_compressible_data-116', '2x_compressible_data-117', '2x_compressible_data-118', '2x_compressible_data-119', '2x_compressible_data-120', '2x_compressible_data-121',
                                '2x_compressible_data-122', '2x_compressible_data-123', '2x_compressible_data-124', '2x_compressible_data-125', '2x_compressible_data-126', '2x_compressible_data-127', '2x_compressible_data-128', '2x_compressible_data-129', '2x_compressible_data-130', '2x_compressible_data-131',
                                '2x_compressible_data-132', '2x_compressible_data-133', '2x_compressible_data-134', '2x_compressible_data-135', '2x_compressible_data-136', '2x_compressible_data-137', '2x_compressible_data-138', '2x_compressible_data-139', '2x_compressible_data-140', '2x_compressible_data-141',
                                '2x_compressible_data-142', '2x_compressible_data-143', '2x_compressible_data-144', '2x_compressible_data-145', '2x_compressible_data-146', '2x_compressible_data-147','2x_compressible_data-148', '2x_compressible_data-149', '2x_compressible_data-150', '2x_compressible_data-151', ]

three_times_compressible_patterns = ['3x_compressible_data-152', '3x_compressible_data-153', '3x_compressible_data-154', '3x_compressible_data-155', '3x_compressible_data-156','3x_compressible_data-157', '3x_compressible_data-158', '3x_compressible_data-159', '3x_compressible_data-160','3x_compressible_data-161',
                                     '3x_compressible_data-162', '3x_compressible_data-163', '3x_compressible_data-164', '3x_compressible_data-165', '3x_compressible_data-166', '3x_compressible_data-167', '3x_compressible_data-168', '3x_compressible_data-169', '3x_compressible_data-170', '3x_compressible_data-171',
                                     '3x_compressible_data-172', '3x_compressible_data-173', '3x_compressible_data-174', '3x_compressible_data-175', '3x_compressible_data-176', '3x_compressible_data-177', '3x_compressible_data-178', '3x_compressible_data-179', '3x_compressible_data-180', '3x_compressible_data-181',
                                     '3x_compressible_data-182', '3x_compressible_data-183', '3x_compressible_data-184', '3x_compressible_data-185', '3x_compressible_data-186', '3x_compressible_data-187', '3x_compressible_data-188', '3x_compressible_data-189', '3x_compressible_data-190', '3x_compressible_data-191',
                                     '3x_compressible_data-192', '3x_compressible_data-193', '3x_compressible_data-194', '3x_compressible_data-195', '3x_compressible_data-196', '3x_compressible_data-197', '3x_compressible_data-198', '3x_compressible_data-199', '3x_compressible_data-200', '3x_compressible_data-201',
                                     '3x_compressible_data-202', '3x_compressible_data-203', '3x_compressible_data-204', '3x_compressible_data-205', '3x_compressible_data-206', '3x_compressible_data-207', '3x_compressible_data-208', '3x_compressible_data-209', '3x_compressible_data-210', '3x_compressible_data-211']


four_times_compressible_patterns = ['4x_compressible_data-212', '4x_compressible_data-213', '4x_compressible_data-214', '4x_compressible_data-215', '4x_compressible_data-216', '4x_compressible_data-217', '4x_compressible_data-218', '4x_compressible_data-219', '4x_compressible_data-220', '4x_compressible_data-221',
                                    '4x_compressible_data-222', '4x_compressible_data-223', '4x_compressible_data-224', '4x_compressible_data-225', '4x_compressible_data-226', '4x_compressible_data-227', '4x_compressible_data-228', '4x_compressible_data-229', '4x_compressible_data-230', '4x_compressible_data-231',
                                    '4x_compressible_data-232', '4x_compressible_data-233', '4x_compressible_data-234', '4x_compressible_data-235', '4x_compressible_data-236', '4x_compressible_data-237', '4x_compressible_data-238', '4x_compressible_data-239', '4x_compressible_data-240', '4x_compressible_data-241',
                                    '4x_compressible_data-242', '4x_compressible_data-243', '4x_compressible_data-244', '4x_compressible_data-245', '4x_compressible_data-246', '4x_compressible_data-247', '4x_compressible_data-248', '4x_compressible_data-249', '4x_compressible_data-250', '4x_compressible_data-251',
                                    '4x_compressible_data-252', '4x_compressible_data-253', '4x_compressible_data-254', '4x_compressible_data-255', '4x_compressible_data-256', '4x_compressible_data-257', '4x_compressible_data-258', '4x_compressible_data-259', '4x_compressible_data-260', '4x_compressible_data-261',
                                    '4x_compressible_data-262', '4x_compressible_data-263', '4x_compressible_data-264', '4x_compressible_data-265', '4x_compressible_data-266', '4x_compressible_data-267', '4x_compressible_data-268', '4x_compressible_data-269', '4x_compressible_data-270', '4x_compressible_data-271']

six_times_compressible_patterns = ['6x_compressible_data-272', '6x_compressible_data-273', '6x_compressible_data-274', '6x_compressible_data-275', '6x_compressible_data-276', '6x_compressible_data-277', '6x_compressible_data-278', '6x_compressible_data-279', '6x_compressible_data-280', '6x_compressible_data-281',
                                   '6x_compressible_data-282', '6x_compressible_data-283', '6x_compressible_data-284', '6x_compressible_data-285', '6x_compressible_data-286', '6x_compressible_data-287', '6x_compressible_data-288', '6x_compressible_data-289', '6x_compressible_data-290', '6x_compressible_data-291',
                                   '6x_compressible_data-292', '6x_compressible_data-293', '6x_compressible_data-294', '6x_compressible_data-295', '6x_compressible_data-296', '6x_compressible_data-297', '6x_compressible_data-298', '6x_compressible_data-299', '6x_compressible_data-300', '6x_compressible_data-301',
                                   '6x_compressible_data-302', '6x_compressible_data-303', '6x_compressible_data-304', '6x_compressible_data-305', '6x_compressible_data-306', '6x_compressible_data-307', '6x_compressible_data-308', '6x_compressible_data-309', '6x_compressible_data-310', '6x_compressible_data-311',
                                   '6x_compressible_data-312', '6x_compressible_data-313', '6x_compressible_data-314', '6x_compressible_data-315', '6x_compressible_data-316', '6x_compressible_data-317', '6x_compressible_data-318', '6x_compressible_data-319', '6x_compressible_data-320', '6x_compressible_data-321',
                                   '6x_compressible_data-322', '6x_compressible_data-323', '6x_compressible_data-324', '6x_compressible_data-325', '6x_compressible_data-326', '6x_compressible_data-327', '6x_compressible_data-328', '6x_compressible_data-329', '6x_compressible_data-330', '6x_compressible_data-331']

eight_times_compressible_patterns = ['8x_compressible_data-332', '8x_compressible_data-333', '8x_compressible_data-334', '8x_compressible_data-335', '8x_compressible_data-336', '8x_compressible_data-337', '8x_compressible_data-338', '8x_compressible_data-339', '8x_compressible_data-340','8x_compressible_data-341',
                                     '8x_compressible_data-342', '8x_compressible_data-343', '8x_compressible_data-344', '8x_compressible_data-345', '8x_compressible_data-346', '8x_compressible_data-347', '8x_compressible_data-348', '8x_compressible_data-349', '8x_compressible_data-350', '8x_compressible_data-351',
                                     '8x_compressible_data-352', '8x_compressible_data-353', '8x_compressible_data-354', '8x_compressible_data-355', '8x_compressible_data-356', '8x_compressible_data-357', '8x_compressible_data-358', '8x_compressible_data-359', '8x_compressible_data-360', '8x_compressible_data-361',
                                     '8x_compressible_data-362', '8x_compressible_data-363', '8x_compressible_data-364', '8x_compressible_data-365', '8x_compressible_data-366', '8x_compressible_data-367', '8x_compressible_data-368', '8x_compressible_data-369', '8x_compressible_data-370', '8x_compressible_data-371',
                                     '8x_compressible_data-372', '8x_compressible_data-373', '8x_compressible_data-374', '8x_compressible_data-375', '8x_compressible_data-376', '8x_compressible_data-377', '8x_compressible_data-378', '8x_compressible_data-379', '8x_compressible_data-380', '8x_compressible_data-381',
                                     '8x_compressible_data-382', '8x_compressible_data-383', '8x_compressible_data-384', '8x_compressible_data-385', '8x_compressible_data-386', '8x_compressible_data-387', '8x_compressible_data-388', '8x_compressible_data-389', '8x_compressible_data-390', '8x_compressible_data-391' ]

twelve_times_compressible_patterns =['12x_compressible_data-392', '12x_compressible_data-393', '12x_compressible_data-394', '12x_compressible_data-395', '12x_compressible_data-396', '12x_compressible_data-397', '12x_compressible_data-398', '12x_compressible_data-399', '12x_compressible_data-400', '12x_compressible_data-401',
                                     '12x_compressible_data-402', '12x_compressible_data-403', '12x_compressible_data-404', '12x_compressible_data-405', '12x_compressible_data-406', '12x_compressible_data-407', '12x_compressible_data-408', '12x_compressible_data-409', '12x_compressible_data-410', '12x_compressible_data-411',
                                     '12x_compressible_data-412', '12x_compressible_data-413', '12x_compressible_data-414', '12x_compressible_data-415', '12x_compressible_data-416', '12x_compressible_data-417', '12x_compressible_data-418', '12x_compressible_data-419', '12x_compressible_data-420', '12x_compressible_data-421',
                                     '12x_compressible_data-422', '12x_compressible_data-423', '12x_compressible_data-424', '12x_compressible_data-425', '12x_compressible_data-426', '12x_compressible_data-427', '12x_compressible_data-428', '12x_compressible_data-429', '12x_compressible_data-430', '12x_compressible_data-431',
                                     '12x_compressible_data-432', '12x_compressible_data-433', '12x_compressible_data-434', '12x_compressible_data-435', '12x_compressible_data-436', '12x_compressible_data-437', '12x_compressible_data-438', '12x_compressible_data-439', '12x_compressible_data-440', '12x_compressible_data-441',
                                     '12x_compressible_data-442', '12x_compressible_data-443', '12x_compressible_data-444', '12x_compressible_data-445', '12x_compressible_data-446', '12x_compressible_data-447', '12x_compressible_data-448', '12x_compressible_data-449', '12x_compressible_data-450', '12x_compressible_data-451',
                                     '12x_compressible_data-452', '12x_compressible_data-453', '12x_compressible_data-454', '12x_compressible_data-455', '12x_compressible_data-456', '12x_compressible_data-457', '12x_compressible_data-458', '12x_compressible_data-459', '12x_compressible_data-460', '12x_compressible_data-461']

sixteen_times_compressible_patterns = ['16x_compressible_data-462', '16x_compressible_data-463', '16x_compressible_data-464', '16x_compressible_data-465', '16x_compressible_data-466', '16x_compressible_data-467', '16x_compressible_data-468', '16x_compressible_data-469', '16x_compressible_data-470', '16x_compressible_data-471',
                                       '16x_compressible_data-472', '16x_compressible_data-473', '16x_compressible_data-474', '16x_compressible_data-475', '16x_compressible_data-476', '16x_compressible_data-477', '16x_compressible_data-478', '16x_compressible_data-479', '16x_compressible_data-480', '16x_compressible_data-481',
                                       '16x_compressible_data-482', '16x_compressible_data-483', '16x_compressible_data-484', '16x_compressible_data-485', '16x_compressible_data-486', '16x_compressible_data-487', '16x_compressible_data-488', '16x_compressible_data-489', '16x_compressible_data-490', '16x_compressible_data-491',
                                       '16x_compressible_data-492', '16x_compressible_data-493', '16x_compressible_data-494', '16x_compressible_data-495', '16x_compressible_data-496', '16x_compressible_data-497', '16x_compressible_data-498', '16x_compressible_data-499', '16x_compressible_data-500', '16x_compressible_data-501',
                                       '16x_compressible_data-502', '16x_compressible_data-503', '16x_compressible_data-504', '16x_compressible_data-505', '16x_compressible_data-506', '16x_compressible_data-507', '16x_compressible_data-508', '16x_compressible_data-509', '16x_compressible_data-510', '16x_compressible_data-511',
                                       '16x_compressible_data-512', '16x_compressible_data-513', '16x_compressible_data-514', '16x_compressible_data-515', '16x_compressible_data-516', '16x_compressible_data-517', '16x_compressible_data-518', '16x_compressible_data-519', '16x_compressible_data-520', '16x_compressible_data-521']


 # generate bit_patterns
with open('00000000-0', 'wb') as f:
    _pattern = int('0', 16).to_bytes(4, 'big')
    f.write(_pattern)

for pattern in bit_patterns:
    _pattern = int(pattern.split('-')[0], 16).to_bytes(4, 'big')
    with open(pattern, 'wb') as f:
        f.write(_pattern)

#  generate byte_patterns
for pattern in byte_patterns:
    _pattern = int(pattern.split('-')[0], 16).to_bytes(4, 'big')
    with open(pattern, 'wb') as f:
        f.write(_pattern)

#  generate word_patterns
for pattern in word_patterns:
    _pattern = int(pattern.split('-')[0], 16).to_bytes(4, 'big')
    with open(pattern, 'wb') as f:
        f.write(_pattern)

#  generate dword_patterns
for pattern in dword_patterns:
    _pattern = int(pattern.split('-')[0], 16).to_bytes(4, 'big')
    with open(pattern, 'wb') as f:
        f.write(_pattern)

 # generate incompressible_patterns
_pattern = bytearray(4096)
for pattern in incompressible_patterns:
    while True:
        for offset in range(4096):
            _pattern[offset] = random.randint(0, 255)
        compress_length = len(zlib.compress(_pattern))
        if compress_length >= 4096:
            break
    with open(pattern, 'wb') as f:
        f.write(_pattern)

#  generate double_compressible_patterns
_pattern = bytearray(4096)
_random_count = 2048
_generated_file = []
for pattern in double_compressible_patterns:
    while True:
        for offset in range(0, 4096):
            _pattern[offset] = 0
        for _ in range(0, _random_count):
            _offset = random.randint(0, 4095)
            _pattern[_offset] = random.randint(0, 255)
        compress_length = len(zlib.compress(_pattern))
        if compress_length == 2048:
            _same_file = False
            for _file in _generated_file:
                with open(_file, "rb") as _f:
                    _file_cont = _f.read()
                    for i in range(8):
                        for j in range(8):
                            if _file_cont[i*512:(i+1)*512] == _pattern[j*512:(j+1)*512]:
                                _same_file = True
            if _same_file:
                continue
            else:
                with open(pattern, 'wb') as f:
                    f.write(_pattern)
                    _generated_file.append(pattern)
                break
        else:
            if compress_length > 2048:
                _random_count -= 1
            else:
                _random_count += 1
#
# #  generate three_times_compressible_patterns
_pattern = bytearray(4096)
_random_count = 4096 // 3
for pattern in three_times_compressible_patterns:
    while True:
        for offset in range(0, 4096):
            _pattern[offset] = 0
        for _ in range(0, _random_count):
            _offset = random.randint(0, 4095)
            _pattern[_offset] = random.randint(0, 255)
        compress_length = len(zlib.compress(_pattern))
        if compress_length == 1365:
            _same_file = False
            for _file in _generated_file:
                with open(_file, "rb") as _f:
                    _file_cont = _f.read()
                    for i in range(8):
                        for j in range(8):
                            if _file_cont[i*512:(i+1)*512] == _pattern[j*512:(j+1)*512]:
                                _same_file = True
            if _same_file:
                continue
            else:
                with open(pattern, 'wb') as f:
                    f.write(_pattern)
                    _generated_file.append(pattern)
                break
        else:
            if compress_length > 1365:
                _random_count -= 1
            else:
                _random_count += 1
#
# #  generate four_times_compressible_patterns
_pattern = bytearray(4096)
_random_count = 4096 // 4
for pattern in four_times_compressible_patterns:
    while True:
        for offset in range(0, 4096):
            _pattern[offset] = 0
        for _ in range(0, _random_count):
            _offset = random.randint(0, 4095)
            _pattern[_offset] = random.randint(0, 255)
        compress_length = len(zlib.compress(_pattern))
        if compress_length == 1024:
            _same_file = False
            for _file in _generated_file:
                with open(_file, "rb") as _f:
                    _file_cont = _f.read()
                    for i in range(8):
                        for j in range(8):
                            if _file_cont[i*512:(i+1)*512] == _pattern[j*512:(j+1)*512]:
                                _same_file = True
            if _same_file:
                continue
            else:
                with open(pattern, 'wb') as f:
                    f.write(_pattern)
                    _generated_file.append(pattern)
                break
        else:
            if compress_length > 1024:
                _random_count -= 1
            else:
                _random_count += 1
#
# #  generate six_times_compressible_patterns
_pattern = bytearray(4096)
_random_count = 4096 // 6
for pattern in six_times_compressible_patterns:
    while True:
        for offset in range(0, 4096):
            _pattern[offset] = 0
        for _ in range(0, _random_count):
            _offset = random.randint(0, 4095)
            _pattern[_offset] = random.randint(0, 255)
        compress_length = len(zlib.compress(_pattern))
        if compress_length == 682:
            _same_file = False
            for _file in _generated_file:
                with open(_file, "rb") as _f:
                    _file_cont = _f.read()
                    for i in range(8):
                        for j in range(8):
                            if _file_cont[i*512:(i+1)*512] == _pattern[j*512:(j+1)*512]:
                                _same_file = True
            if _same_file:
                continue
            else:
                with open(pattern, 'wb') as f:
                    f.write(_pattern)
                    _generated_file.append(pattern)
                break
        else:
            if compress_length > 682:
                _random_count -= 1
            else:
                _random_count += 1
#
# #  generate eight_times_compressible_patterns
_pattern = bytearray(4096)
_random_count = 4096 // 8
for pattern in eight_times_compressible_patterns:
    while True:
        for offset in range(0, 4096):
            _pattern[offset] = 0
        for _ in range(0, _random_count):
            _offset = random.randint(0, 4095)
            _pattern[_offset] = random.randint(0, 255)
        compress_length = len(zlib.compress(_pattern))
        if compress_length == 512:
            _same_file = False
            for _file in _generated_file:
                with open(_file, "rb") as _f:
                    _file_cont = _f.read()
                    for i in range(8):
                        for j in range(8):
                            if _file_cont[i*512:(i+1)*512] == _pattern[j*512:(j+1)*512]:
                                _same_file = True
            if _same_file:
                continue
            else:
                with open(pattern, 'wb') as f:
                    f.write(_pattern)
                    _generated_file.append(pattern)
                break
        else:
            if compress_length > 512:
                _random_count -= 1
            else:
                _random_count += 1
#
# #  generate twelve_times_compressible_patterns
_pattern = bytearray(4096)
_random_count = 4096 // 12
for pattern in twelve_times_compressible_patterns:
    while True:
        for offset in range(0, 4096):
            _pattern[offset] = 0
        for _ in range(0, _random_count):
            _offset = random.randint(0, 4095)
            _pattern[_offset] = random.randint(0, 255)
        compress_length = len(zlib.compress(_pattern))
        if compress_length == 341:
            _same_file = False
            for _file in _generated_file:
                with open(_file, "rb") as _f:
                    _file_cont = _f.read()
                    for i in range(8):
                        for j in range(8):
                            if _file_cont[i*512:(i+1)*512] == _pattern[j*512:(j+1)*512]:
                                _same_file = True
            if _same_file:
                continue
            else:
                with open(pattern, 'wb') as f:
                    f.write(_pattern)
                    _generated_file.append(pattern)
                break
        else:
            if compress_length > 341:
                _random_count -= 1
            else:
                _random_count += 1
#
#
# #  generate sixteen_times_compressible_patterns
_pattern = bytearray(4096)
_random_count = 4096 // 16
for pattern in sixteen_times_compressible_patterns:
    while True:
        for offset in range(0, 4096):
            _pattern[offset] = 0
        for _ in range(0, _random_count):
            _offset = random.randint(0, 4095)
            _pattern[_offset] = random.randint(0, 255)
        compress_length = len(zlib.compress(_pattern))
        if compress_length == 256:
            _same_file = False
            for _file in _generated_file:
                with open(_file, "rb") as _f:
                    _file_cont = _f.read()
                    for i in range(8):
                        for j in range(8):
                            if _file_cont[i*512:(i+1)*512] == _pattern[j*512:(j+1)*512]:
                                _same_file = True
            if _same_file:
                continue
            else:
                with open(pattern, 'wb') as f:
                    f.write(_pattern)
                    _generated_file.append(pattern)
                break
        else:
            if compress_length > 256:
                _random_count -= 1
            else:
                _random_count += 1