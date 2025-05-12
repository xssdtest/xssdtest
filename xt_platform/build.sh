#!/usr/bin/env bash
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
TRACK_FILE="platform_diff"
DEFAULT_FILES=(
    "xt_platform/xt_interface.pxd"
    "xt_platform/setup.py"
    "xt_platform/xt_interface.pyx"
    "xt_platform/xt_random.pyx"
    "xt_platform/src"
)

declare -A commit_ids
declare -A diff_contents
need_rebuild=false

load_records() {
    if [ -f "$TRACK_FILE" ] && [ -s "$TRACK_FILE" ]; then
        while IFS='|' read -r path base_id base_diff; do
            commit_ids["$path"]="$base_id"
            diff_contents["$path"]="$(echo -e "$base_diff")"
        done < <(sed 's/\x1F/\n/g' "$TRACK_FILE")
    else
        for path in "${DEFAULT_FILES[@]}"; do
            commit_ids["$path"]=""
            diff_contents["$path"]=""
        done
        need_rebuild=true
    fi
}

save_records() {
    : > "$TRACK_FILE"
    for path in "${!commit_ids[@]}"; do
        encoded_diff=$(echo -n "${diff_contents[$path]}" | sed ':a;N;$!ba;s/\n/\x1F/g')
        echo "${path}|${commit_ids[$path]}|$encoded_diff" >> "$TRACK_FILE"
    done
}

load_records

for path in "${!commit_ids[@]}"; do
    current_commit=$(git log -1 --pretty=format:%H "$path" 2>/dev/null)
    current_diff=$(git diff "$path" 2>/dev/null)

    [ -z "$current_commit" ] && current_commit="NEW_FILE"

    if [ "${commit_ids[$path]}" != "$current_commit" ]; then
        commit_ids["$path"]="$current_commit"
        diff_contents["$path"]="$current_diff"
        need_rebuild=true
    else
        if [ "${diff_contents[$path]}" != "$current_diff" ]; then
            diff_contents["$path"]="$current_diff"
            need_rebuild=true
        fi
    fi
done

if $need_rebuild; then
    save_records
    chmod 644 "$TRACK_FILE"; sync;
    pushd src || { echo "Cannot enter src directory"; exit 1; }
    make || { echo "Make failed"; exit 1; }
    popd || { echo "Cannot return to previous directory"; exit 1; }

    if [ -d "build" ]; then
        rm -fr build
    fi
    /home/anaconda3/bin/python setup.py build_ext --inplace || { echo "Build failed"; exit 1; }
    echo "Changes detected, need to rebuild."
else
    if ls /path/to/dir/xt_random*.so >/dev/null 2>&1 && \
       ls /path/to/dir/xt_interface*.so >/dev/null 2>&1; then
        echo "No changes detected."
    else
        /home/anaconda3/bin/python setup.py build_ext --inplace || { echo "Build failed"; exit 1; }
    fi
fi
