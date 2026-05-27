#include <bits/stdc++.h>
using namespace std;

int main(){
    ifstream in("input.txt");
    ofstream out("output.cpp");

    out<<"#include <iostream>\nusing namespace std;\nint main(){\n";

    string line;
    while(getline(in,line)){
        stringstream ss(line);
        vector<string> t;
        string w;

        while(ss>>w) t.push_back(w);
        if(t.size()==0) continue;

        if(t[0]=="let"){
            if(t.size()==4)
                out<<"int "<<t[1]<<"="<<t[3]<<";\n";
            else if(t.size()==6)
                out<<t[1]<<"="<<t[3]<<t[4]<<t[5]<<";\n";
        }
        else if(t[0]=="print"){
            out<<"cout<<"<<t[1]<<"<<endl;\n";
        }
        else if(t[0]=="if"){
            out<<"if("<<t[1]<<" "<<t[2]<<" "<<t[3]<<"){\n";
        }
        else if(t[0]=="else"){
            out<<"}else{\n";
        }
        else if(t[0]=="while"){
            out<<"while("<<t[1]<<" "<<t[2]<<" "<<t[3]<<"){\n";
        }
        else if(t[0]=="for"){
            out<<"for(int "<<t[1]<<"="<<t[3]<<";"<<t[1]<<"<="<<t[5]<<";"<<t[1]<<"++){\n";
        }
        else if(t[0]=="end"){
            out<<"}\n";
        }
    }

    out<<"return 0;}";
}
