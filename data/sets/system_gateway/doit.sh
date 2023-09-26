#!/usr/bin/env bash
set -e

set_name="System Gateway"
sheet_url="https://access.nullsignal.games/Gateway/English/English/SystemGatewayEnglish-A4%20Printable%20Sheets%201x.pdf"
sheet_file="SystemGatewayEnglish-A4 Printable Sheets 1x.pdf"
sheet_idxs="002 004 006 008 010 012 014 016 018 020"
width=743
height=1030
start_x=77
start_y=77
num_x=3
num_y=3
card_idx=1
bleed=1
set_id=30

echo "Initialising card images for ${set_name}..."
cd "$(dirname "$0")"

if [ ! -f "${sheet_file}" ]
then
    wget "${sheet_url}" -o "${sheet_file}"
fi

echo "Got sheet file"

if [ ! -d ./sheets ]
then
    mkdir sheets
    pdfimages -png "${sheet_file}" sheets/sheet
fi

echo "Extracted sheets"

for sheet_idx in $sheet_idxs
do
    for y_idx in $(seq 0 $(( ${num_y} - 1 )) )
    do
        for x_idx in $(seq 0 $(( ${num_x} - 1 )) )
        do
            x=$(( ${start_x} + ( ${x_idx} * (${width} + ${bleed} ) ) ))
            y=$(( ${start_y} + ( ${y_idx} * (${height} + ${bleed} ) ) ))

            nrdb_url=https://netrunnerdb.com/api/2.0/public/card/${set_id}$(printf "%03d" $card_idx )
            name=$(curl -s ${nrdb_url} | jq --raw-output .data[0].title )

            if [ "$name" != "null" ]
            then
                convert sheets/sheet-${sheet_idx}.png\
                    -crop ${width}x${height}+${x}+${y}\
                    "cards/${name}.png"
                echo "Produced card: $name"
            fi

            card_idx=$(( ${card_idx} + 1 ))
        done
    done
done

echo "${set_name} ready!"
