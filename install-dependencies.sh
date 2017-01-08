#!/usr/bin/env sh

cd ~
mkdir sdl2install
mkdir sdl2install/bin
mkdir sdl2install/lib
export SDL2DIR="`pwd`/sdl2install"
export SDL_CONFIG=$SDL2DIR/bin
export PYSDL2_DLL_PATH=$SDL2DIR/lib
export PATH=$PATH:$PYSDL2_DLL_PATH:$SDL2DIR:$SDL_CONFIG:


# install sdl2-2.0.5 
wget https://www.libsdl.org/release/SDL2-2.0.5.tar.gz
tar xf SDL2-2.0.5.tar.gz
cd SDL2-2.0.5  
./configure --prefix=$SDL2DIR
make
sudo make install
cd ..

# install SDL2_image-2.0.1
wget https://www.libsdl.org/projects/SDL_image/release/SDL2_image-2.0.1.tar.gz
tar xf SDL2_image-2.0.1.tar.gz
cd SDL2_image-2.0.1
./configure --prefix=$SDL2DIR
make
sudo make install
cd ..

# install SDL2_ttf-2.0.14
wget https://www.libsdl.org/projects/SDL_ttf/release/SDL2_ttf-2.0.14.tar.gz
tar xf SDL2_ttf-2.0.14.tar.gz
cd SDL2_ttf-2.0.14
./configure --prefix=$SDL2DIR
make
sudo make install
cd ..

# install SDL2_mixer-2.0.1
wget https://www.libsdl.org/projects/SDL_mixer/release/SDL2_mixer-2.0.1.tar.gz
tar xf SDL2_mixer-2.0.1.tar.gz
cd SDL2_mixer-2.0.1
./configure --prefix=$SDL2DIR
make
sudo make install
cd ..

# install SDL2_gfx-1.0.1
wget http://www.ferzkopp.net/Software/SDL2_gfx/SDL2_gfx-1.0.1.tar.gz
tar xf SDL2_gfx-1.0.1.tar.gz
cd SDL2_gfx-1.0.1
./configure --prefix=$SDL2DIR
make
sudo make install
cd ..

ls $PYSDL2_DLL_PATH
