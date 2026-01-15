The transformation of human-readable C++ source code into an executable program is not instantaneous. It occurs through a pipeline of distinct steps where the output of one stage becomes the input for the next. While a command like `g++` or `gcc` appears to do this in one go, it actually invokes a sequence of tools: the preprocessor (`cpp`), the compiler proper (`cc1`), the assembler (`as`), and the linker (`collect2` or `ld`).

C++ has many compilation flags which are options passed to the compiler to control the compilation process, enabling several more features. Here are some common flags that GNU and Clang compilers include:

- `-std=c++XX`: Specifies the C++ language standard to use (e.g., `-std=c++17`, `-std=c++20`).
- `-Wall`: Enables a large set of common and useful warnings.
- `-Wextra`: Enables extra warnings not included in `-Wall`.
- `-Wpedantic`: Issues all warnings required by the ISO C++ standard and warns about non-standard extensions.
- `-Werror`: Treats all warnings as compilation errors, forcing them to be fixed.
- `-Wconversion`: Warns about implicit conversions that may change the value or sign of a data type.
- `-Wshadow`: Warns when a local variable shadows another variable (local, parameter, or global).
- `-Wunused`: Warns about unused variables or functions.
- `-O0`: No optimization; faster compilation, ideal for debugging.
- `-O1`, `-O2`, `-O3`: Increasing levels of optimization, with `-O3` being the most aggressive for maximum performance. However, `-O3` may use a lot of randomized optimizations which can potentially slow it down a lot too. For most cases, `-O2` is the best advised optimization option.
- `-Ofast`: Enables even higher-level optimizations than `-O2` and `-O3`, including some that may not strictly conform to the C++ standard (e.g., fast but inaccurate floating-point arithmetic).
- `-g`: Generates debugging symbols in the compiled code, which is essential for using a debugger (e.g., GDB).
- `-o <filename>`: Specifies the name of the output file (e.g., `g++ main.cpp -o program` creates an executable named `program`).

As an example, I want to use a very simple C (not C++) program throughout the explanation of the compilation model. Unless mentioned otherwise, everything we’ll see about C also applies to C++ (which was designed with C compatibility in mind). Our program, reproduced below in full, is a complete implementation of a modular read-only “database” of the number of passengers on a set of flights. Take a moment to understand it fully, as we will be using this program throughout the explanation of the compilation model.

```c
// paxDB.h
int getCount(char* flightNumber, int deflt);


// paxDB.c
#include "paxDB.h"

int flights[] = { 20, 15, 0 };

#define GET(n) if (flightNumber[0] == #n[0]) return flights[n]

int getCount(char* flightNumber, int deflt)
{
    GET(0);
    GET(1);
    GET(2);
    return deflt;
}


// paxCount.c
#include "paxDB.h"

int main(int argc, char** argv)
{
    if (argc > 1)
        return getCount(argv[1], -1);

    return 0;
}


// paxCheck.c
#include "paxDB.h"
#define ERROR 1
#define SUCCESS 0

int main(int argc, char** argv)
{
    int count = 0;

    if (argc > 1)
        count = getCount(argv[1], 0);

    if (count == 0)
        return ERROR;
    else
        return SUCCESS;
}
```

`paxCount.c` takes one command-line argument: A flight number, like 0 or 1 or 2 (in fact those are the only flights in our database). The program returns, as its shell exit status, the number of passengers on the specified flight.

```shell
$ gcc -Wall -Werror paxCount.c paxDB.c && ( ./a.out 1 ; echo $? )
15
```

`paxCheck.c` takes the flight number on the command line, and returns success if the flight is in the database and has any passengers, or error otherwise (note that to the shell, a zero exit code means success, and non-zero means error).

```shell
$ gcc -Wall -Werror -o paxCheck paxCheck.c paxDB.c

$ ./paxCheck 1 && echo "OK" || echo "ERROR"
OK

$ ./paxCheck 5 && echo "OK" || echo "ERROR"
ERROR
```

---

# 1. Preprocessing

The preprocessor handles directives that begin with the `#` symbol. This stage operates purely on text manipulation before the code is syntactically analyzed.

You can stop the compiler after this stage using the `-E` flag while compiling the source code to view the preprocessed output. Examples will be shown below.

<ul>
   <li>
      <p><strong>Input:</strong> Source code file (e.g., <code>paxCount.cpp</code>).</p>
   </li>
   <li>
      <p><strong>File Inclusion (<code>#include</code>):</strong> The preprocessor replaces <code>#include</code> directives with the full textual content of the specified header file. This is a literal &quot;copy and paste&quot; operation. This allows a program to be split into multiple files, where header files (<code>.h</code> or <code>.hpp</code>) provide interface declarations. We could call our file <code>paxDB.not-a-header</code> and say <code>#include &quot;paxDB.not-a-header&quot;</code> instead, and it’s still a header file. The <code>.h</code> / <code>.hpp</code> suffix is just a convention. What the compiler proper sees is exactly the same (bar those <code>#</code> comments) as our original paxCount.c (the one that declared getCount directly instead of #includeing the header file).</p>
      
```shell
$ gcc -E -Wall -Werror paxCount.c
# 1 "paxCount.c"
# 1 "<built-in>"
# 1 "<command-line>"
# 1 "paxCount.c"
# 1 "paxDB.h" 1
int getCount(char* flightNumber, int deflt);
# 2 "paxCount.c" 2

int main(int argc, char** argv)
{
    if (argc > 1)
        return getCount(argv[1], -1);

    return 0;
}
```

   </li>
   <li>
      <strong>Macro Expansion (<code>#define</code>):</strong> It replaces defined constants or macros with their specific values or code snippets. Macros act as text substitution, which differs significantly from runtime function calls. <code>#define</code> can also take parameters, to create preprocessor macros as shown by the examples below.
      
```shell
$ gcc -E -Wall -Werror paxCheck.c
# 1 "paxCheck.c"
# 1 "<built-in>"
# 1 "<command-line>"
# 1 "paxCheck.c"
# 1 "paxDB.h" 1
int getCount(char* flightNumber, int deflt);
# 2 "paxCheck.c" 2

int main(int argc, char** argv)
{
    int count = 0;

    if (argc > 1)
        count = getCount(argv[1], 0);

    if (count == 0)
        return 1;
    else
        return 0;
}


$ gcc -E -Wall -Werror paxDB.c
# 1 "paxDB.c"
# 1 "<built-in>"
# 1 "<command-line>"
# 1 "paxDB.c"
# 1 "paxDB.h" 1
int getCount(char* flightNumber, int deflt);
# 2 "paxDB.c" 2

int flights[] = { 20, 15, 0 };

int getCount(char* flightNumber, int deflt)
{
    if (flightNumber[0] == "0"[0]) return flights[0];
    if (flightNumber[0] == "1"[0]) return flights[1];
    if (flightNumber[0] == "2"[0]) return flights[2];
    return deflt;
}


$ gcc -Wall -Werror -o paxCount  paxCount.c paxDB.c

$ ./paxCount 1 ; echo $?
15
```

   </li>
   <li>
      <strong>Conditional Compilation (<code>#ifdef</code> and <code>#ifndef</code>):</strong> These directives can be used to allow specific parts of the code to be compiled or ignored based on certain conditions.
      <ul>
         <li>The <code>ifdef</code> (if defined) directive checks if a preprocessor macro exists and if it is defined, the code block between <code>#ifdef</code> and <code>#endif</code> (or <code>#else</code>) is compiled, or else the preprocessor removes it before the compiler sees it.</li>
         <li>On the other hand, the <code>#ifndef</code> (if not defined) directive checks if a preprocessor macros doesn&#39;t exist and if it is not defined, the code block is compiled, or else the preprocessor removes it before the compiler sees it. You can also use the <code>#ifndef</code>, and <code>#define</code> directives as include guards to prevent compilation errors caused by including the same header file multiple times in a single translational unit. This is more likely to happen on large codebases, where a <code>.cpp</code> file includes many header files, and one of those in turn includes a header file already included earlier on. Include guards do not affect the inclusion into separate translation units, so they won’t help if you are seeing duplicate symbol errors at link time.</li>
         <li>The <code>#if</code> directive works similar to an if statement. However, It can only deal with preprocessor stuff which is basically preprocessor macros (which are either function like or constant-like) and C tokens with some simple integer-literal arithmetic.</li>
      </ul>

```c
#define DEBUG // Macro is defined
#ifdef DEBUG
    printf("Debugging is on\n"); // This will be compiled
#endif

// paxDB.h (include guard example)
#ifndef __PAX_DB_H__ // If header file not defined before...
#define __PAX_DB_H__ // Define it now:

int getCount(char* flightNumber, int deflt);

#endif
```

   </li>
   <li>
      <p><strong>Comment Removal:</strong> All comments are stripped from the code.</p>
   </li>
   <li>
      <p><strong>Output:</strong> A "Translational Unit" (often with a <code>.i</code> extension). This file contains no directives or comments, just pure c++ code ready for the compiler.</p>
   </li>
</ul>


# Step 2: Compilation (The "Front End")

The compiler is a program that takes high level language (in our case: C++) as input, and translates it to a intermediate representation (in our case: Assembly Language). The process of compilation takes place in several phases: 

- Frontend: Source Code -> Lexer -> Parser -> Semantic Analyzer -> Optimizer -> Code Generator -> Assembly Code
- Backend: Assembly Code -> Assembler -> Linker -> Machine Code

Right now, we will only explore the "compile proper" which will handle the frontend of the compilation process.

You can stop the compiler after this stage using the `-S` flag while compiling the source code to view the assembly. Examples will be shown below.

![frontend](https://i.imgur.com/ZipcVGN.png)

Let's dive deeper into the substeps involving analysis and synthesis:

<ol>
   <li>
      <p>Lexical Analysis (Scanning)</p>
      <ul>
         <li>The scanner reads the input character stream (character at a time) and groups characters into meaningful &quot;lexical units&quot; called tokens (e.g., identifiers, keywords, operators like <code>+</code> or <code>:=</code>).</li>
         <li>It ignores whitespace and detects lexical errors (e.g., invalid characters not in the language&#39;s alphabet).</li>
      </ul>
   </li>
   <li>
      <p>Syntax Analysis (Parsing)</p>
      <ul>
         <li>The parser analyzes the stream of tokens to determine the grammatical structure of the program. While the lexer identifies and distinguishes individual tokens between identifiers, keywords, literals, operators, and symbols, the parser identifies groups of tokens as statements, expressions, declarations, etc.</li>
         <li>Based on the syntax grammar, the syntax analyzer constructs a hierarchical structure called a parse tree (or syntax graph) that represents the syntax.</li>
         <li>If a grammar allows multiple parse trees for a single string, it is ambiguous. However, most parsers, including c++, use precedence rules to resolve this (e.g., <code>*</code> binds tighter than <code>+</code>).</li>
      </ul>
   </li>
   <li>
      <p>Symbol Table &amp; Context Analysis (Context)</p>
      <ul>
         <li>The compiler maintains a database called &#39;The Symbol Table&#39; to store attributes of identifiers (variables, functions, classes), such as their type, scope, and memory addresses (offsets). The lexical and syntax analyzer perform various operations to interact with the symbol table. For example, they perform an <code>insert</code> operation when a variable is declared, a <code>lookup</code> operation when a variable is used, and a <code>delete</code> operation when a symbol is no longer needed.</li>
         <li>The symbol table is important for the context analyzer and it may perform many <code>lookup</code> operations on the symbol table during this stage but no modifications.</li>
         <li>The context analyzer also ensures semantic correctness, such as checking if a variable is declared before use or if types in an expression are compatible.</li>
      </ul>
      <img src="https://i.imgur.com/VKsEtYL.png" alt="analysis" height="400" />
   </li>
   <li>
      <p>Intermediate Code Generation &amp; Optimization (Semantics)</p>
      <ul>
         <li>The semantics analyzer may translate the parse tree into an Intermediate Representation (IR), such as an abstract syntax tree or a psuedo-assembly code (e.g., P-code).</li>
         <li>The compiler optimizes this IR to make the program smaller or faster (e.g., removing redundant calculations) before generating the full assembly.</li>
      </ul>
   </li>
   <li>
      <p>Code Generation (Assembly Output)</p>
      <ul>
         <li>The internal representation is translated into assembly instructions specific to the target architecture (x86, ARM).</li>
         <li>In C++, function names are &quot;mangled&quot; (encoded with type information) to support function overloading and namespaces. For example, <code>getCount(int)</code> might become <code>__Z8getCounti</code>. This is not available in C.</li>
         <li>As the last stage of the compiler, we generate an assembly file (with a <code>.s</code> extension) as the output.</li>
      </ul>
   </li>
</ol>

# Step 3: Assembly

The assembler translates the human-readable assembly code into object code (machine instructions). The compiler comes from your compiler vendor (in this case, GNU), whereas the assembler comes with your system. This implies that the assembler must create object files in a format that the linker will understand (on Linux, and many other systems, this is the "Executable and Linkable Format", or ELF). We will talk more about the linker in depth shortly, but for now just know the linker merges multiple object files into a single executable file.

CPU architectures are defined by their Instruction Set Architecture (ISA), primarily split into CISC (Complex Instruction Set Computer, e.g., x86 for Intel/AMD) and RISC (Reduced Instruction Set Computer, e.g., ARM, RISC-V), with RISC focusing on simplicity for efficiency, while CISC uses complex instructions for high code density, plus modern trends like multi-core, heterogeneous (big.LITTLE) designs, and specialized cores for different tasks. The assembler uses the ISA according to the CPU architecture to generate the object files.

You can use the `-c` flag to perform the compiling and assembly, but stop before the linking. Other tools like `objdump` or `nm` can be used to inspect object files.

```shell
$ gcc -c -Wall -Werror paxCount.c paxDB.c

$ nm paxCount.o
                 U _getCount
0000000000000000 T _main

$ nm paxDB.o
0000000000000058 D _flights
0000000000000000 T _getCount


# We can link the object files together using `gcc` (which calls `ld` behind the scenes)
$ gcc -Wall -Werror paxCount.o paxDB.o

$ ls a.out
a.out

$ ./a.out 1 ; echo $?
15
```

<ul>
   <li><strong>Input:</strong> Assembler code from the compiler (all the individual <code>.s</code> files generated)</li>
   <li>
      <strong>Process:</strong> The process runs 2 passes through the assembler code.
      <ol>
         <li>
             Pass through the object code and build a symbol table mapping labels (e.g., function names) to memory offsets. <img src="https://i.imgur.com/Zq2Xjsu.png" alt="pass1" height=400 />
         </li>
         <li>
             Pass through the object code again and translate mnemonics (like <code>ADD</code> or <code>MOV</code>) into binary opcodes and resolve addresses. <img src="https://i.imgur.com/D60wKIi.png" alt="pass2" height=400 />
         </li>
      </ol>
   </li>
   <li><strong>Output:</strong> For each assembler file provided as input, an object file (<code>.o</code> or <code>.obj</code>) is produced. This is a binary file containing machine code, but it is not yet executable because it may reference symbols (functions/variables) location in other files. The object files contain sections for Code (Text), Data, and a Symbol Table (listing defined and undefined symbols).</li>
</ul>

*Note:* You rarely need to think about compilation and assembly as two separate stages. Personally, my main use case for looking at the assembler code is to figure out what optimizations the compiler is and isn’t performing.

# Step 4: Linking

The linker is responsible for combining one or more object files and libraries into a single Executable File.

- **Input:** All the individual object files (`.o` or `.obj`) produced by the assembler.
- **Symbol Resolution:** The linker resolves references. If `FileA.o` calls a function `calculate()` defined in `FileB.o`, the linker connects the call site in A to the definition in B. It replaces all the placeholder addresses in the individual object files with real memory addresses (or offsets).
    - If a definition could not be found, the linker issues an "undefined reference" error. If multiple definitions exist for the same symbol (violating the One Definition Rule), a "duplicate symbol" error occurs.
- **Standard Libraries:** The linker connects your C++ code with Standard Template Library (STL) functions by matching function/variable symbols (names) between your compiled object files and pre-compiled library files (like `libstdc++.a` or `msvcrt.lib`). When the compiler sees `std::cout << "Hi";`, it generates a reference to an `_Z4cout...` symbol (mangled name) in your code's object file, but doesn't know where it lives. The linker finds the actual machine code for `_Z4cout` within the C++ standard library's object files/libraries, resolves the reference by substituting the correct memory address, and bundles everything into a single executable, creating calls to the library's concrete code.
- **Output:** A single executable file with machine code according to your CPU's ISA (`.out` for linux, `.exe` for windows).

### Internal vs External Linkage

When we looked at the symbols in `paxDB.o` using the `nm` tool:

```shell
$ nm paxDB.o
0000000000000058 D _flights
0000000000000000 T _getCount
```

The `D` in front of the symbol `flights` indicates that it is in the **data section** of the object file. The **upper-case** `D` indicates that it is external. We say that `flights` has "external linkage" which means that code outside of `paxDB.c`'s translation unit can access `flights` by name.

```c
// paxCount.c
#include "paxDB.h"

extern int flights[];

int main(int argc, char** argv)
{
    flights[1]++;

    if (argc > 1)
        return getCount(argv[1], -1);

    return 0;
}
```

```shell
$ gcc -Wall -Werror -o paxCount  paxCount.c paxDB.o

$ ./paxCount 1 ; echo $?
16
```

The `extern` keyword declares that `flights` is an array of ints defined somewhere else. This line of code works as a declaration rather than a definition because it contains the `extern` specifier, and it doesn't have an initializer). So when we linked the two object files together, `paxCount.o` was able to change the array in `paxDB.o`.

In `paxDB.c` we can disable outside access to the `flights` array by giving it "internal linkage". In C++, you can give global symbols internal linkage with `static`, `const`, or  wrapping them in unnamed namespaces (we'll explore this soon). If you look at the symbols in `paxDB.o`, we see that `flights` is internal now (the `d` is lower-case).

```c
// paxCount.c
#include "paxDB.h"

static int flights[] = { 20, 15, 0 }; // or
// const int flights[] = { 20, 15, 0 };
// by c++ standard, global const objects automatically get internal linkage (effectively static const)

int getCount(char* flightNumber, int deflt)
{
    if (flightNumber[0] == '0') return flights[0];
    if (flightNumber[0] == '1') return flights[1];
    if (flightNumber[0] == '2') return flights[2];
    return deflt;
}
```

```shell
$ gcc -c -Wall -Werror paxDB.c

$ nm paxDB.o
0000000000000058 d _flights
0000000000000000 T _getCount


$ gcc -c -Wall -Werror paxCount.c

$ gcc -Wall -Werror -o paxCount  paxCount.o paxDB.o
Undefined symbols:
  "_flights", referenced from:
      _main in paxCount.o
      _main in paxCount.o
ld: symbol(s) not found
collect2: ld returned 1 exit status
```

Note: Even with internal linkage, you can reference a function or variable if you somehow know its address. Internal linkage simply stops you from referring to it by name (which, for most purposes, is all that really matters).

### Linking C++ with C Libraries

What happens if we update our `paxCount` program from C to C++ but our `paxDB` code (being used by other programs) can't be updated that easily? Can we still link C libraries to C++ programs somehow?

Let's define our new `paxCount.cpp` program and see what happens when we try to link our program to the old `paxDB` library:

```cpp
// paxCount.cpp
#include "paxDB.h"

int main(int argc, char** argv)
{
    if (argc > 1)
        return getCount(argv[1], -1);

    return 0;
}
```

```shell
$ g++ -c -Wall -Werror paxCount.cpp

$ g++ -Wall -Werror -o paxCount  paxCount.o paxDB.o
Undefined symbols:
  "getCount(char*, int)", referenced from:
      _main in paxCount.o
ld: symbol(s) not found
collect2: ld returned 1 exit status

$ nm paxDB.o
0000000000000058 d _flights
0000000000000000 T _getCount

$ nm paxCount.o
                 U __Z8getCountPci
0000000000000000 T _main
```

We can see that there is a mismatch in the symbol names since C doesn't mangle the function names as it doesn't provide function overloading capabilities. We can fix this situation by declaring that `getCount` from `paxDB` has C linkage.

```cpp
// paxCount.cpp
extern "C" {
#include "paxDB.h"
}

int main(int argc, char** argv)
{
    if (argc > 1)
        return getCount(argv[1], -1);

    return 0;
}
```

```shell
$ g++ -c -Wall -Werror paxCount.cpp

$ nm paxCount.o
                 U _getCount
0000000000000000 T _main

$ g++ -Wall -Werror -o paxCount  paxCount.o paxDB.o

$ ./paxCount 1 ; echo $?
15
```

### Namespaces

A namespace is a logical container that groups names (like classes, functions, or variables) to prevent naming conflicts, similar to how folders organize files, allowing the same name to be used in different contexts without confusion.

To explain linkage with namespaces let's define a new simple cargo database program:

```cpp
// cargoDB.h
int getCount(char* flightNumber, int deflt);

// cargoDB.cpp
#include "cargoDB.h"

static int flights[] = { 0, 8, 9 };

int getCount(char* flightNumber, int deflt)
{
    if (flightNumber[0] == '0') return flights[0];
    if (flightNumber[0] == '1') return flights[1];
    if (flightNumber[0] == '2') return flights[2];
    return deflt;
}
```

As you surely noticed, the interface and implementation of the cargo database are identical to the passenger database. Only the data is different (flights 0, 1 and 2 have 0, 8 and 9 cargo containers, compared to 20, 15 and 0 passengers, respectively). However, since we chose the same name for our interface (getCount) we won’t be able to use the cargo database together with the passenger database; both versions of getCount take exactly the same arguments, so even with name mangling there will be a conflict. For example if we try to link cargoDB and paxDB with paxCount:

```shell
$ g++ -c -Wall -Werror paxDB.cpp

$ g++ -c -Wall -Werror cargoDB.cpp

$ g++ -c -Wall -Werror paxCount.cpp

$ g++ -Wall -Werror -o paxCount  paxCount.o paxDB.o cargoDB.o
ld: duplicate symbol getCount(char*, int)in cargoDB.o and paxDB.o
collect2: ld returned 1 exit status
```

This error is due to the one definition rule: “Every program shall contain exactly one definition of every non-inline function or object that is used in that program.” We can use namespaces to help us here. We can group related functions and data in a namespace, and we can disambiguate between the different `getCount`s by using the appropriate namespace name:

```cpp
// paxDB.h
namespace pax
{
int getCount(char* flightNumber, int deflt);
}

// paxDB.cpp
#include "paxDB.h"

static int flights[] = { 20, 15, 0 };

int pax::getCount(char* flightNumber, int deflt)
{
    if (flightNumber[0] == '0') return flights[0];
    if (flightNumber[0] == '1') return flights[1];
    if (flightNumber[0] == '2') return flights[2];
    return deflt;
}

// cargoDB.h
namespace cargo
{
int getCount(char* flightNumber, int deflt);
}

// cargoDB.cpp
#include "cargoDB.h"

static int flights[] = { 0, 8, 9 };

int cargo::getCount(char* flightNumber, int deflt)
{
    if (flightNumber[0] == '0') return flights[0];
    if (flightNumber[0] == '1') return flights[1];
    if (flightNumber[0] == '2') return flights[2];
    return deflt;
}
```

```shell
$ g++ -c -Wall -Werror paxDB.cpp

$ nm paxDB.o
0000000000000058 d __ZL7flights
0000000000000000 T __ZN3pax8getCountEPci

$ g++ -c -Wall -Werror cargoDB.cpp

$ nm cargoDB.o
0000000000000058 d __ZL7flights
0000000000000000 T __ZN5cargo8getCountEPci
```

You can see above how the C++ compiler incorporates the namespace names into its name mangling. Note also that the two different `flights` arrays don't conflict, because they have internal linkage so they are local to their own translation unit.

For the internal linkage of items under a namespace, the C++ standard recommends using unnamed (or anonymous) namespaces:

```cpp
// paxDB.cpp
#include "paxDB.h"

namespace
{
int flights[] = { 20, 15, 0 };
}

int pax::getCount(char* flightNumber, int deflt)
{
    if (flightNumber[0] == '0') return flights[0];
    if (flightNumber[0] == '1') return flights[1];
    if (flightNumber[0] == '2') return flights[2];
    return deflt;
}

// cargoDB.cpp
#include "cargoDB.h"

namespace
{
int flights[] = { 0, 8, 9 };
}

int cargo::getCount(char* flightNumber, int deflt)
{
    if (flightNumber[0] == '0') return flights[0];
    if (flightNumber[0] == '1') return flights[1];
    if (flightNumber[0] == '2') return flights[2];
    return deflt;
}
```

```shell
$ g++ -c -Wall -Werror paxDB.cpp

$ nm paxDB.o
0000000000000058 d __ZN12_GLOBAL__N_17flightsE
0000000000000000 T __ZN3pax8getCountEPci

$ g++ -c -Wall -Werror cargoDB.cpp

$ nm cargoDB.o
0000000000000058 d __ZN12_GLOBAL__N_17flightsE
0000000000000000 T __ZN5cargo8getCountEPci
```

Unnamed namespaces have an implicit using directive placed at the translation unit’s global scope. Depending on your compiler implementation, names inside an unnamed namespace will be given internal linkage; or the compiler will generate a random namespace name (guaranteed to be unique) and be given external linkage. It seems our compiler chooses the internal linkage method, with the same generated name for both unnamed namespaces instead of generating random unique namespace names.

### Static vs Dynamic Linking

Multiple object files can be packaged together into a single archive called a static library. You can use the `ar` tool to bunch object files into **static libraries**.

```shell
$ g++ -c -Wall -Werror paxDB.cpp cargoDB.cpp
$ ar -r libFlightDBs.a  paxDB.o cargoDB.o

$ nm libFlightDBs.a | c++filt

libFlightDBs.a(paxDB.o):
0000000000000058 d (anonymous namespace)::flights
0000000000000000 T pax::getCount(char*, int)

libFlightDBs.a(cargoDB.o):
0000000000000058 d (anonymous namespace)::flights
0000000000000000 T cargo::getCount(char*, int)
```

As a library supplier, you would deliver the archive file together with the relevant header files (`paxDB.h` and `cargoDB.h`).

The linker will look inside archive files specified with the `-l` flag (with the `lib` prefix and `.a` suffix dropped), and it looks for them in the locations specified with the `-L` flag. Unlike straight object files specified on the command line, the linker will only link the symbols actually used. In this example `paxCount.cpp` doesn't use any symbols from `cargoDB.cpp` and therefore they are not included:

```shell
$ g++ -Wall -Werror -o paxCount -L. -lFlightDBs  paxCount.cpp
/usr/bin/ld: /tmp/ccyIWP4h.o: in function `main':
paxCount.cpp:(.text+0x2d): undefined reference to `pax::getCount(char*, int)'
collect2: error: ld returned 1 exit status
# read note below to see why

$ g++ -Wall -Werror -o paxCount -L. paxCount.cpp -lFlightDBs
# success!

$ nm paxCount | c++filt
0000000100001068 d (anonymous namespace)::flights
0000000100000e4c T pax::getCount(char*, int)
0000000100000ea4 T _main
```

Note: When linking several such libraries, and one library references symbols defined in another library, the order you specify the libraries on the command line matters. If library A refers to symbols in library B, the linker needs to have processed A before it gets to B.

The process of linking static libraries within the executable file is called **static linking**.

On the other hand, when a library is used by many different programs (think, for example, of the C Posix library), copying the used functions into each executable program is an inefficient use of disk and memory. Functions in **shared libraries** aren’t linked into an executable program directly; instead, the linker generates code that, at run time, will look up the address of the shared library’s symbols. The run-time overhead is minimal (only one extra jump, via a jump table containing the addresses of all shared library symbols used by the program). At run time, only one copy of the shared library needs to be loaded in memory, regardless of how many different programs are using it. Another advantage is that a shared library can be upgraded independently of the programs that use it (as long as the library’s interface hasn’t changed).

To generate a shared library, the object files must be compiled with the `-fPIC` option, which tells `gcc` to generate position independent code (so that, for example, function calls won’t depend on the function definition being at a particular position in memory). To build the shared library, we use gcc’s `-shared` flag.

```shell
$ g++ -shared -fPIC -o libFlightDBs.so  paxDB.cpp cargoDB.cpp

$ nm libFlightDBs.so | c++filt
0000000000001014 d (anonymous namespace)::flights
0000000000001008 d (anonymous namespace)::flights
0000000000000e50 T pax::getCount(char*, int)
0000000000000ea8 T cargo::getCount(char*, int)
0000000000000000 t __mh_dylib_header
                 U dyld_stub_binder
```

Let's slightly tweak our `paxCount.cpp` program to use the `pax::getCount` definition from the shared library and we can see that the function definition isn’t included in the program binary (`U` before the `pax::getCount` symbol when `nm` debugging):

```cpp
#include "paxDB.h"

int main(int argc, char** argv)
{
    if (argc > 1)
        return pax::getCount(argv[1], -1);

    return 0;
}
```

```shell
$ g++ -fPIC -Wall -Werror -o paxCount -L. -lFlightDBs  paxCount.cpp

$ nm paxCount | c++filt
                 U pax::getCount(char*, int)
0000000100000ee4 T _main
```

When we execute the program, the OS first loads the executable into memory. If the program uses shared libraries, the OS invokes the **dynamic linker** (or loader) which loads the required shared libraries into memory as well. The dynamic loader searches for libraries in standard locations like `/usr/lib`, as well as (on Linux) the directories specified by the environment variable `LD_LIBRARY_PATH`. If the shared libraries are already loaded into memory, then it links that pre-loaded library to the executable, meaning it won't load shared libraries into memory more than once at a time. On Linux, `ldd` (list dynamic dependencies) will print the shared libraries required by the program:

```shell
$ ldd -v paxCount
        linux-vdso.so.1 (0x00007ffcc89a5000)
        libFlightDBs.so (0x00007396bf4e6000)
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007396bf200000)
        /lib64/ld-linux-x86-64.so.2 (0x00007396bf4f2000)

        Version information:
        ./paxCount:
                libc.so.6 (GLIBC_2.2.5) => /lib/x86_64-linux-gnu/libc.so.6
                libc.so.6 (GLIBC_2.34) => /lib/x86_64-linux-gnu/libc.so.6
        /lib/x86_64-linux-gnu/libc.so.6:
                ld-linux-x86-64.so.2 (GLIBC_2.2.5) => /lib64/ld-linux-x86-64.so.2
                ld-linux-x86-64.so.2 (GLIBC_2.3) => /lib64/ld-linux-x86-64.so.2
                ld-linux-x86-64.so.2 (GLIBC_PRIVATE) => /lib64/ld-linux-x86-64.so.2
```

---

# Makefile Automation

A **makefile** contains a set of rules. Each rule specifies a **target** (or multiple targts), **prerequisites**, and a **recipe** (a shell command) for generating the target from its prerequisites.

```makefile
# define variables that can be used with $()
CXX = g++
CXXFLAGS = -Wall -Wextra -Werror -fPIC

# format of a makefile rule:
# target_name: prerequisite list (optional)
#    run_recipe_shell_command

all: paxCount

paxCount: paxCount.cpp paxDB.h libFlightDBs.so
	$(CXX) $(CXXFLAGS) -o $@ paxCount.cpp -L. -lFlightDBs

libFlightDBs.so: paxDB.o cargoDB.o
	$(CXX) -shared -o $@ $^

# Static pattern rule
paxDB.o cargoDB.o: %.o: %.cpp %.h
	$(CXX) -c $(CXXFLAGS) $<

clean:
	rm -f paxCount libFlightDBs.so *.o
```

When you run `make` (with no arguments), it automatically runs the first target defined in the Makefile, which is conventionally named `all` and typically builds everything needed for the project. In this case, the first rule defines only the `paxCount` prerequisite which refers to the second rule with the `paxCount` target.

The second rule specifies how to build the `paxCount` executable (the recipe should look very familiar to you). The recipe must be preceded by exactly one tab (not spaces). The recipe will be re-run whenever `paxCount.cpp` or `libFlightDBs.so` changes and `make` is called (make compares the timestamps of the prerequisites against the timestamp of the target).

The third rule specifies how to build the shared library. It uses make’s automatic variables, where `$@` means the name of the target and `$^` means the names of all the prerequisites with spaces between them.

The fourth rule is a **pattern rule**. Its effect is the same as specifying separate rules for each of the object files: A rule with target `paxDB.o` and prerequisites `paxDB.cpp` and `paxDB.h`; and another similar rule for `cargoDB.o`. It uses the automatic variable `$<` which means the name of the first prerequisite (in this case the `%.cpp` prerequisite files).

The final rule specifies how to remove all generated files. It has no prerequisites so it will be run whenever you specify the target name (`make clean`).

If we run `make`, make will figure out from the prerequisites that it needs to build `libFlightDBs.so`; and to build that, it needs to build `paxDB.o` and `cargoDB.o`.

```shell
$ make
g++ -c -Wall -Wextra -Werror -fPIC paxDB.cpp
g++ -c -Wall -Wextra -Werror -fPIC cargoDB.cpp
g++ -shared -o libFlightDBs.so paxDB.o cargoDB.o
g++ -Wall -Wextra -Werror -fPIC -o paxCount paxCount.cpp -L. -lFlightDBs
```

If we run `make` again, it won’t do anything because none of the source files have changed. But if they have changed, `make` will rebuild only the targets affected:

```shell
$ make
make: Nothing to be done for 'all'.

$ rm paxDB.o 

$ make
g++ -c -Wall -Wextra -Werror -fPIC paxDB.cpp
g++ -shared -o libFlightDBs.so paxDB.o cargoDB.o
g++ -Wall -Wextra -Werror -fPIC -o paxCount paxCount.cpp -L. -lFlightDBs
```

In large projects, tracking the prerequisites of a `.cpp` file manually becomes impossible (every header included by the file is a prerequisite). To solve this, it seems makefiles have default hidden rules that can automatically build files properly (examples shown below). `g++ -M` will generate a list of prerequisites in makefile format. Makefiles already use this feature by default to build files that aren't targetted by any custom defined rules. However, if you like having control over your make rules, you can use the output of `g++ -M` which already comes in the proper Makefile rule format.

```shell
$ make paxDB.o paxCount.o
g++ -c -Wall -Wextra -Werror -fPIC paxDB.cpp
g++ -Wall -Wextra -Werror -fPIC   -c -o paxCount.o paxCount.cpp

# as we can see the paxDB.o rule worked properly, but paxCount.o also worked by default
# even though there is no such rule specified by our makefile.

$ g++ -M paxDB.cpp
paxDB.o: paxDB.cpp paxDB.h
```

---

# Resources

**Online:**
- [learncpp.com](https://www.learncpp.com) - comprehensive free tutorial
- [godbolt.org](https://godbolt.org) - compiler explorer
- [david.rothlis.net](https://david.rothlis.net/c/compilation_model/) - thorough c++ study

**Videos:**
- https://youtu.be/ksJ9bdSX5Yo - video explanation w/ examples

