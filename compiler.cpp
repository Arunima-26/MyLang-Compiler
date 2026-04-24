#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <set>
using namespace std;

vector<string> tokenize(string line) {
    vector<string> tokens;
    stringstream ss(line);
    string word;
    while (ss >> word) tokens.push_back(word);
    return tokens;
}

int main() {
    ifstream file("input.mylang");
    ofstream out("output.cpp");

    set<string> declared;
    string line;
    int lineNo = 0;

    out << "#include <iostream>\nusing namespace std;\n\nint main() {\n";

    while (getline(file, line)) {
        lineNo++;
        vector<string> t = tokenize(line);
        if (t.empty()) continue;

        if (t[0] == "start" || t[0] == "stop") continue;

        else if (t[0] == "let") {
            string var = t[1];

            if (declared.find(var) == declared.end()) {
                out << "    int " << var << ";\n";
                declared.insert(var);
            }

            if (t.size() == 4) {
                out << "    " << var << " = " << t[3] << ";\n";
            } else if (t.size() == 6) {
                out << "    " << var << " = "
                    << t[3] << " " << t[4] << " " << t[5] << ";\n";
            }
        }

        else if (t[0] == "print") {
            out << "    cout << " << t[1] << " << endl;\n";
        }

        else if (t[0] == "if") {
            out << "    if(" << t[1] << " " << t[2] << " " << t[3] << ") {\n";
        }

        else if (t[0] == "else") {
            out << "    } else {\n";
        }

        else if (t[0] == "while") {
            out << "    while(" << t[1] << " " << t[2] << " " << t[3] << ") {\n";
        }

        else if (t[0] == "for") {
            out << "    for(int " << t[1] << " = " << t[3] << "; "
                << t[1] << " <= " << t[5] << "; "
                << t[1] << "++) {\n";
        }

        else if (t[0] == "end") {
            out << "    }\n";
        }

        else {
            cout << "Error at line " << lineNo << ": Unknown keyword '" << t[0] << "'\n";
        }
    }

    out << "    return 0;\n}";
    file.close();
    out.close();

    cout << "Compilation successful! output.cpp generated.\n";
    return 0;
}