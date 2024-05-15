dirs=(
"./05052024_2151/"
"./05052024_2242/"
"./05052024_2256/"
"./06052024_0759/"
"./06052024_1128/"
)

# Loop over the array
for dir in "${dirs[@]}"; do
    python3 ./main.py -i "$dir"
done