#!/usr/bin/env sh
set -e

sheet_url="https://nullsignal.games/wp-content/uploads/2022/07/Midnight-Sun-Final-PNP-A4-English-1x.pdf"
set_name="Midnight Sun"
sheet_file="Midnight-Sun-Final-PNP-A4-English-1x.pdf"
sheet_start=13
sheet_end=77
card_idx=1
set_id=33

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

for sheet_idx in $(seq ${sheet_start} ${sheet_end} )
do
    nrdb_url=https://netrunnerdb.com/api/2.0/public/card/$(printf "%02d%03d" ${set_id} ${card_idx})
    name=$(curl -s ${nrdb_url} | jq --raw-output .data[0].title )

    if [ "$name" != "null" ]
    then
        cp sheets/sheet-$(printf "%03d" $sheet_idx).png "cards/${name}.png"
    fi

    card_idx=$(( ${card_idx} + 1 ))
done

echo "${set_name} ready!"
