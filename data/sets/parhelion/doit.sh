#!/usr/bin/env bash

set -e

set_name="Parhelion"
sheet_url="https://access.nullsignal.games/Gateway/English/English/SystemGatewayEnglish-A4%20Printable%20Sheets%201x.pdf"
sheet_file="ParhelionEnglish-A4-Printable-Sheets-1x-1.pdf"
sheet_start=0
sheet_end=67
card_idx=66
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
        echo "Produced card: $name"
    fi

    if [ ${sheet_idx} -ge 28 -a ${sheet_idx} -le 32 ]
    then
        # matryoshka hack >:(
        # Because of the slightly hacky way I'm counting this and the fact that
        # the 1x PDF contains six copies of Matryoshka, we need to wind back the
        # card index to make sure we accurately identify all the cards after
        # Matryoshka
        card_idx=$(( ${card_idx} - 1 ))
    fi

    card_idx=$(( ${card_idx} + 1 ))
done

echo "${set_name} ready!"
