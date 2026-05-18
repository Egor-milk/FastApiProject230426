docker rm /booking_db 


docker network create my_network

linux
docker run --name booking_db \
    -p 6432:5432 \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=48erons2445 \
    -e POSTGRES_DB=booking2 \
    --network=my_network \
    --volume pg-booking-data:/var/lib/postgresql \
    -d postgres



windows

docker run --name booking_db `
    -p 6432:5432 `
    -e POSTGRES_USER=postgres `
    -e POSTGRES_PASSWORD=48erons2445 `
    -e POSTGRES_DB=booking2 `
    --network=my_network `
    --volume pg-booking-data:/var/lib/postgresql `
    -d postgres:18.3

docker run --name booking_cache `
    -p 7379:6379 `
    --network=my_network `
    -d redis:8.0.5

docker run --name booking_back `
    -p 7777:8000 `
    --network=my_network `
    booking_image

docker build -t booking_image .