xhost +local:root
docker-compose up --build -d && docker-compose run UMAT_2scale_LSDYNA && docker-compose down
xhost -local:root

# docker compose build --progress plain && docker run -it my_umat_lsdyna_image
