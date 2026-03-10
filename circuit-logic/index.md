This journey takes us "From Zero to One," starting with the simplest building blocks of 1s and 0s and culminating in a functioning computer.
One of the characteristics that separates an engineer or computer scientist from a layperson is a systematic approach to managing complexity.
Modern digital systems are built from millions or billions of transistors. No human being could understand these systems by writing equations describing the movement of electrons in each transistor and solving all of the equations simultaneously.
To truly understand how a microprocessor is created, you will need to learn to manage complexity using two systematic principles: abstraction and discipline.

**Abstraction** is a technique that hides details that aren't important. A system can be viewed from many different levels of abstraction.

Various levels of abstraction for an electronic computing system along with the typical building blocks at each level:

| Application Software | Operating Systems | Architecture | Microarchitecture | Logic | Digital Circuits | Analog Circuits | Devices | Physics |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Programs | Device Drivers | Instructions, Registers | Datapaths, Controllers | Adders, Memories | AND gates, NOT gates | Amplifiers, Filters | Transistors, Diodes | Electrons |

At the lowest level of abstraction is the *physics*, the motion of electrons. The behavior of electrons is described by quantum mechanics and Maxwell's equations.
Our system is constructed from electronic *devices* such as transistors (or vacuum tubes, once upon a time).
These devices have well-defined connection points called terminals and can be modeled by the relationship between voltage and current as measured at each terminal.
By abstracting to this level, we can ignore the individual electrons.
The next level of abstraction is *analog circuits*, in which devices are assembled to create components such as amplifiers.
Analog circuits input and output a continuous range of voltages.
*Digital circuits* such as logic gates restrict the voltages to discrete ranges, which we will use to indicate 0 or 1.
In *logic* design, we build more complex structures, such as adders or memories, from digital circuits.

*Microarchitecture* links the logic and architecture levels of abstraction.
The *architecture* level of abstraction describes a computer from the programmer's perspective.
For example, the Intel IA-32 architecture used by microprocessors in most personal computers (PCs) is defined by a set of instructions and registers (memory for temporarily storing variables) that the programmer is allowed to use.
Microarchitecture involves combining logic elements to execute the instructions defined by the architecture.
A particular architecture can be implemented by one of many different microarchitectures with different price/performance/power trade-offs.
For example, the Intel Core 2 Duo, the Intel 80486, and the AMD Athlon all implement the IA-32 architecture with different microarchitectures.

Moving into the software realm, the *operating system* handles low-level details such as accessing a hard drive or managing memory.
Finally, the *application software* uses these facilities provided by the operating system to solve a problem for the user.
Thanks to the power of abstraction, we can surf the web without any regard for the quantum vibrations of electrons of the organization of memory in the computer.

In here, I want to focus on the lower levels of abstraction from **analog circuits** and **logic**. When you are working at one level of abstraction, it is good to know something about the levels directly above and below it. For example, a computer scientist cannot fully optimize code without understanding the architecture for which the program is being written.

**Discipline** is the act of intentionally restricting your design choices so that you can work more productively at a higher level of abstraction.
Digital circuits use discrete voltages, whereas analog circuits use continuous voltages.
Therefore digital circuits are a subset of analog circuits and in some sense must be capable of less than the broader class of analog circuits.
However, digital circuits are much simpler to design.
By limiting ourselves to digital circuits, we can easily combine components into sophisticated systems that ultimately outperform those built from analog components in many applications.
Like how, digital televisions and cell phones are replacing their analog predecessors.

---

# 1. Analog Circuits

Analog circuits are electronic systems that process continuous signals (representing real-world data like sound, temperature, or light) using components such as resistors, capacitors, diodes, and transistors.
They operate on a continuous range of voltage or current, allowing for functions like amplification, filtering, and signal conditioning.
Unlike digital circuits, analog circuits are more susceptible to noise but are essential for interfacing with a physical world.

While most physical variables in the real world (voltage, frequency, or position) are continuous (analog), digital systems abstract this information into discrete-valued variables.
Basically, what I am trying to say is that digital circuits are continuous too, since they too are built from analog components like transistors.
However, we simply abstract their continuous values into discrete valued 1s and 0s to make them digital circuits. This abstraction helps lay the groundwork to start building microprocessors.
So this might have you questioning: what is the difference between digital and analog circuits since all circuits are analog anyway?

![signaltimeline](https://i.imgur.com/SwC3QUn.png)

In a twisted way, analog circuits are digital circuits without the abstraction. We need their continuous values sometimes to gain more information that we can't from digital circuits.
For example, when a computer interacts with the physical world through sensors (like a microphone picking up sound or a thermometer measuring heat), the electrical signals it receives are usually tiny (millivolts).
They are usually also full of electromagnetic noise since electrons fluctuate very randomly and continuous variables are susceptible to noise.
A microprocessor's Analog-to-Digital Converter (ADC) might not be able to read these signals raw signals accurately.

Signal conditioning is the process of amplifying the tiny signal so the processor can see it, and filtering the noise so the processor doesn't process garbage data.
I want to briefly deep dive into the analog components that are responsible for any signal conditioning that occurs within analog circuits.
I will not be diving into the working principles of these devices or components.

## Amplification

<!-- TODO: introduce what amplification is and why it is important -->
<!-- TODO: talk about operational amplifiers and how they work as comparators and how they work as inverting amplifiers and noninverting amplifiers -->
<!-- TODO: talk about negative feedback loops and why op-amps need them for inverted or noninverted amplification -->

## Filtering

<!-- TODO: read up on filtering and plan notes to take -->

---

# 2. Digital Circuits

---

# 3. Logic

---

# Resources

---

*Written by BooleanCube :]*
