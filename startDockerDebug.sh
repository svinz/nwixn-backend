docker build -t int2:debug  --target debug .
echo "Time to run the debugger!!"
docker run --rm -it -p 5678:5678 --name debugger int2:debug 
