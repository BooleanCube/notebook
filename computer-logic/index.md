"There are 10 kinds of people: those who understand binary and those who can't."
To move from the latter group to the former requires undertaking a specific journey: creation of the microprocessor.
While the inner workings of these chips often seem like "magic" to the uninitiated, they are actually the result of straightforward engineering once carefully explained.
Indeed, designing and building a microprocessor is considered a "special rite of passage" for computer science and engineering students, bridging the gap between hardware and software.

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

In here, I want to mainly focus on the levels of abstraction from **digital circuits** through **computer architecture**. When you are working at one level of abstraction, it is good to know something about the levels directly above and below it. For example, a computer scientist cannot fully optimize code without understanding the architecture for which the program is being written.

**Discipline** is the act of intentionally restricting your design choices so that you can work more productively at a higher level of abstraction.
Digital circuits use discrete voltages, whereas analog circuits use continuous voltages.
Therefore digital circuits are a subset of analog circuits and in some sense must be capable of less than the broader class of analog circuits.
However, digital circuits are much simpler to design.
By limiting ourselves to digital circuits, we can easily combine components into sophisticated systems that ultimately outperform those built from analog components in many applications.
Like how, digital televisions and cell phones are replacing their analog predecessors.

## Intuitive Understanding of Electricity

When beginning to explore the world of computers, it is vital to start by understanding the basics of electricity and charge.
Before we can dive deeper into higher layers of abstraction, we must ensure a deep understanding of what electrical charge is, and how we measure it with voltage, current, and resistance.

Electrical charge is a basic property of subatomic particles that occurs when electrons are transferred from one particle to another.
An object becomes charged when it gains or loses electrons, creating an imbalance.
Charged objects exert electromagnetic forces (attraction and repulsion) on each other, and the movement of charge is called electric current.

In short, voltage is the electrical 'pressure' that pushes electrical charges (electrons) to flow through a circuit, current is the rate at which charge is flowing, and resistance is a material's tendency to resist the flow of charge (current).

However, while these definitions provide a basic understanding of how we measure electricity, I wanted to deeply understand the intuition behind what causes electricity to flow in a circuit.
We define voltage as the difference in charge (electrons) between two points in a circuit.
This difference in potential puts the electrons under pressure to flow in the direction of current. Without voltage there is no current.

I want to use a common analogy, a water tank, to help visualize this better.
In this analogy, charge is represented by the water amount, voltage is represented by the water pressure, and current is represented by the water flow.

![wateranalogy](https://cdn.sparkfun.com/assets/e/8/8/4/8/5113d1c3ce395fc87d000000.png)
*This is a water tank at a certain height above the ground. At the bottom of this tank there is a hose.*

The pressure at the end of the hose can represent voltage. The water in the tank represents charge.
The more water in the tank, the higher the charge, the more pressure is measured at the end of the hose.

We can think of this tank as a battery, a place where we store a certain amount of energy and then release it.
If we drain our tank a certain amount, the pressure created at the end of the hose goes down.
We can think of this a as a decreasing voltage, like when a flashlight gets dimmer as the batteries run down.
There is also a decrease in the amount of water that will flow through the hose.
Less pressure means less water is flowing, which brings us to current.

# 1. Digital Circuits

Before diving into the specific components, it is helpful to understand the context of **digital circuits**.
While most physical variables in the real world (voltage, frequency, or position) are continuous (analog), digital systems abstract this information into discrete-valued variables.
Specifically, electronic computers generally use a binary representation, where a high enough voltage indicates a `1 (TRUE)` and a low enough voltage indicates a `0 (FALSE)`.

This digital abstraction allows designers to focus on the logical manipulation of 1s and 0s without constantly solving complex physics equations describing the motion of electrons in every component.
Digital circuits are the physical implementations of this logic, restricting voltages to discrete ranges to represent binary states.

## CMOS Transistors

Modern digital circuits are primarily built using **transistors**, which act as electronically controlled switches that turn ON and OFF when voltage or current is applied to a control terminal.
The two main types of transistors are *bipolar transistors* and *metal-oxide-semiconductor field effect transistors* (MOSFETs or MOS transistors, pronounced "moss-fets" or "M-O-S", respectively).
The specific technology used for the vast majority of chips today is known as CMOS (Complementary MOS).
To understand how these switches work, we must look at the underlying materials and components: semiconductors, diodes, and capacitors.

- **Semiconductors**: CMOS technology relies on Silicon (Si), a group IV atom (so it has four electrons in its valence shell and forms bonds with four adjacent atoms) that forms a crystalline lattice. Pure silicon turns out to be a poor conductor, so engineers add impurities called **dopants** to alter its conductivity. Adding Arsenic (group V) creates **n-type** silicon, which has free negatively charged electrons. Adding Boron (group III) creates **p-type** silicon, which has "holes" (missing electrons) that act like positive charge carriers.
![semiconductors](https://i.imgur.com/1qnjdDw.png)

- **Diodes**: When n-type and p-type silicon are joined, the form a **diode**. A diode acts as a one-way valve for current. The p-type region is called the anode and the n-type region is called the cathode. When the voltage on the anode rises above the voltage on the cathode, the diode is forward biased, and current flows through the diode from the anode to the cathode. But wen the anode voltage is lower than the voltage on the cathode, the diode is reverse biased, and no current flows.

---

# Resources

- [csl.cornell.edu/courses/ece2300](https://www.csl.cornell.edu/courses/ece2300/readings.html)
- [learn.sparkfun.com](https://learn.sparkfun.com/tutorials/voltage-current-resistance-and-ohms-law/all)
- "Digital Design and Computer Architecture, RISC-V Edition," by D. M. Harris and S. L. Harris (Morgan Kaufmann, 2021)
- [Making logic gates from transistors - YouTube](https://youtu.be/sTu3LwpF6XI)
