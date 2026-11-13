#include <iostream>
#include <boost/tokenizer.hpp>
#include <fstream>
#include <vector>
#include <algorithm>
#include <chrono>

#define MAX_TABLE_SIZE 100000

static int colcount = 0;

struct Data {
	unsigned int count;
	std::string strdata;
};

struct Cells {
	std::vector<Data> data; //slow because it copies data every time it realoc
	bool occ = false;               // perhaps ill use link list
};

void readFile(std::string &dest, const char* f);

unsigned long djb2(std::string &key);

void addColData(std::string &p_data, Cells &p_cells);

void addNewData(std::string &p_data, Cells &p_cells);

int main() {
	std::string content;
	readFile(content, "akjv.txt");

	// init 
	Cells cells[MAX_TABLE_SIZE];

	auto start = std::chrono::high_resolution_clock::now();
	typedef boost::tokenizer<> Tok;
	Tok tok(content);
	std::cout << "Tokenizing.. (" <<
		std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::high_resolution_clock::now() - start).count() <<
		"ms)" << std::endl;
		
	// count token
	int tcount = 0;
	for (auto i = tok.begin(); i != tok.end(); ++i) {
		tcount += 1;
	}

	unsigned long key;
	start = std::chrono::high_resolution_clock::now();
    for (std::string i : tok) {
    	key = djb2(i)%MAX_TABLE_SIZE;
    	if (cells[key].occ) {
    		addColData(i, cells[key]);
    	}
    	else {
    		cells[key].occ = true;
    		addNewData(i, cells[key]);
    	}
    }
	std::cout << "Hashing.. (" <<
			std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::high_resolution_clock::now() - start).count() <<
			"ms)" << std::endl;

    // flatten the array for display
    start = std::chrono::high_resolution_clock::now();
    std::vector<Data> arr;
    for (auto i : cells) {
    	if (i.occ) {
    		for (size_t j = 0; j < i.data.size(); j++) {
    			arr.push_back(i.data[j]);
    		}
    	}
    }
	std::cout << "Flattening.. (" <<
			std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::high_resolution_clock::now() - start).count() <<
			"ms)" << std::endl;

	// sort
    start = std::chrono::high_resolution_clock::now();
	std::sort(arr.begin(), arr.end(), 
		[](Data &a, Data &b) {
			return a.count > b.count;
		});
	std::cout << "Sorting.. (" <<
			std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::high_resolution_clock::now() - start).count() <<
			"ms)" << std::endl;
    
	std::cout << "\nToken Count: " << tcount << std::endl;
	std::cout << "Unique Tokens: " << arr.size() <<std::endl;
	std::cout << "Collusion Count: " << colcount <<std::endl;

	std::cout << "Top Most Frequent Words:" << std::endl;
    for (size_t i = 0; i < 5; i++) {
    	
    	std::cout << i+1 << ":" << std::endl;
    	std::cout << "---------" << std::endl;
    	std::cout << "Word: " << arr[i].strdata << std::endl;
    	std::cout << "Count: " << arr[i].count << std::endl;
    	std::cout << "---------" << std::endl;
    	
    }
    return 0;
}


void readFile(std::string &dest, const char* f) {
	std::ifstream file(f);
	
	std::string c;
	while (std::getline(file, c)) {
		dest += c;
	}
	file.close();
}

unsigned long djb2(std::string &key) {
	unsigned long hash = 5381;
	for (size_t i = 0; i < key.size(); i++) {
		hash = hash * 33 + (int)key[i];
	}
	return hash;
}

void addColData(std::string &p_data, Cells &p_cells) {
	// find the data and increment the counter
	for (size_t i = 0; i < p_cells.data.size(); i++) {
		if (p_cells.data[i].strdata == p_data) {
			p_cells.data[i].count += 1;
			return;
		}
	}
	// no data entry in the cell yet, so we push one
	colcount += 1;
	addNewData(p_data, p_cells);
}

void addNewData(std::string &p_data, Cells &p_cells) {
	Data d = {.count = 1, .strdata = p_data};
	p_cells.data.push_back(d);
}
