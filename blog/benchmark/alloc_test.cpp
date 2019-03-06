#include <ctime>
#include <iostream>

class Obj {
	int i1;
	int i2;
	int i3; 
	char a2;
	long l1;
	long ar[10];
};
static const int COUNT = 100000;

static Obj** create_objs() {
	int c = COUNT;
	Obj** r = new Obj*[c];
	for (int i = 0; i < c; i++) {	
		r[i] = new Obj();	
	}
	return r;
}

static Obj** create_objs_on_buf() {
	int c = COUNT, s = sizeof(Obj);
	int buf_size = s * c;
	Obj** r = new Obj*[c];
	uint8_t* buf = static_cast<uint8_t*>(malloc(buf_size));
	uint8_t* start = buf;
	for (int i = 0; i < c; i++) {
		// printf("test\n");
		r[i] = new (start) Obj;
		start += s;
	} 	
	return r;		
}

int main(int argc, char *argv[]) {
	std::clock_t start;
    start = std::clock();
	auto r = create_objs_on_buf();	
	std::cout << "Time: " << (std::clock() - start) << " ticks" << std::endl;
    return 0;
}