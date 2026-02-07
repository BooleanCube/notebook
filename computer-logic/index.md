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

In here, I want to focus on the lower levels of abstraction from **physics** through **logic**. When you are working at one level of abstraction, it is good to know something about the levels directly above and below it. For example, a computer scientist cannot fully optimize code without understanding the architecture for which the program is being written.

**Discipline** is the act of intentionally restricting your design choices so that you can work more productively at a higher level of abstraction.
Digital circuits use discrete voltages, whereas analog circuits use continuous voltages.
Therefore digital circuits are a subset of analog circuits and in some sense must be capable of less than the broader class of analog circuits.
However, digital circuits are much simpler to design.
By limiting ourselves to digital circuits, we can easily combine components into sophisticated systems that ultimately outperform those built from analog components in many applications.
Like how, digital televisions and cell phones are replacing their analog predecessors.

---

# 1. Physics Behind Electricity

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

![wateranalogy](https://cdn.sparkfun.com/assets/e/8/8/4/8/5113d1c3ce395fc87d000000.png) <br>
*This is a water tank at a certain height above the ground. At the bottom of this tank there is a hose.*

The pressure at the end of the hose can represent voltage. The water in the tank represents charge.
The more water in the tank, the higher the charge, the more pressure is measured at the end of the hose.

We can think of this tank as a battery, a place where we store a certain amount of energy and then release it.
If we drain our tank a certain amount, the pressure created at the end of the hose goes down.
We can think of this a as a decreasing voltage, like when a flashlight gets dimmer as the batteries run down.
There is also a decrease in the amount of water that will flow through the hose.
Less pressure means less water (current) is flowing.

Batteries are designed to provide a specific amount of voltage, and while bulbs itself don't have voltage, they require a specific voltage (electrical pressure) to work.
Rather, voltage is supplied to it from the electrical system for it to function, converting that electrical energy into light and heat.
Voltage is the "push" that makes current flow through the bulb's filament or LED, causing it to light up.

## Voltage Intuition

I feel like even with these definitions of voltage as a potential difference, it is not very intuitive how exactly it works within circuits.
After many many days of searching for answers I found some analogies that finally make sense and I wanted to share.

In a standard single-loop circuit (like a series of Christmas lights), voltage is "spent" as current flows through resistive components.
In the real world, even the copper wire acts as a resistor, though super weak.
While we often pretend wires are perfect conductors in circuit diagrams (0 Ohms), physically, copper is not a super conductor.
It resists the flow of electrons slightly, which causes a slight loss of energy (voltage) as the current travels from one end to the other.
Copper atoms vibrate, and in doing so collide with moving electrons. Every collision loses a bit of energy to heat or other forms. This loss of energy manifests a slight Voltage drop.
If you run electricity through a long distance wire, the resistance can add up over time, and reduce the voltage received on the other end.

I want to use a ski slope as an analogy to explain how voltage works in a single-loop circuit.
Imagine the battery as a ski lift taking you to the top of the mountain (10V).
Every resistor or light bulb represents a slope, and as you ski down a slope, you lose height.
At the very top of the mountain, let's say you are at 10V. After the first resistor, you could be measured at 7V. After the second resistor, you might be at 3V.
And at the bottom of the mountain, you are measured at 0V.
In this analogy, voltage represents the height difference between you and the **ground**.
This concept of **GND** (ground) can also be commonly found within most circuit diagrams and it represents the point of lowest voltage in the entire circuit (0 V, end of the flow of current).

When a wire splits into two or more branches, the voltage across each branch is the exact same.
All branches connect to the same split point, and reunion point, therefore the potential difference must be the identical.
Think of it as a river flowing downhill. The stream hits an island and splits into 2 streams: Stream A is wide and clear, Stream B is narrow and rocky.
The river splits into 2 streams that both start at the same height and both streams merge again at the same height too.
Using this analogy, the drop in height (voltage) for both streams should be equal since they have the same starting and finishing elevation, even though one stream might carry much more water (current).
No matter how many slopes (resistors) a stream (parallel path) may encounter on the hill, it will drop the same height (voltage) as the other stream (other parallel path).

Using height to visualize voltage and gravity to visualize the pressure of voltage, made voltage extremely more intuitive for me.

## Pulling Voltage (Current Intuition)

This is a short one, but I wanted to briefly go over this because it is important to remember.
Now, throughout this article voltage is described as the force that "pushes" electrons (or electrical charges) throughout the circuit.
That is actually accurate, but I would like to clarify a common misconception this creates when it comes to the flow of electrons.
People commonly visualize the flow of electrons in a circuit as being pushed out of a power source, but this is unintuitive to understand in electricity sometimes.
A better approach to visualize it is: to see the electrons being pulled by the ground from the power source (the other way around), like tug of war.
This works well with the gravitational force analogy for voltage as well since gravity is a force that pulls (not pushes).
This is more intuitive when explaining why current doesn't flow in open circuits and explaining other mistakes where current is misinterpreted/misused.

I'm guessing that is why current is conventionally shown flowing from the positive terminal to the negative terminal of a battery even though the flow of electrons is in the opposite direction.
That definitely makes it much easier to visualize electron flow.
Also conventionally, the positive terminal of a battery actually represents a high voltage and the negative terminal represents ground.
This might seem unintuitive at first because the positive terminal actually feels the least electrical pressure (voltage definition) to move electrons.
When a point has a higher voltage than another point in a circuit, it basically means that it is more positive (has less electrical charge).
This works well with the pulling perspective of current, since a point of higher voltage has a stronger pull on electrons than a point of lower voltage.

So please keep this in mind throughout the article and whenever you think about current visually.

## Ohm's Law

To further explain the relationship between voltage, current, and resistance: <br>
![ohmsanalogy](https://cdn.sparkfun.com/assets/7/6/4/b/6/5113dc8fce395fe201000001.png)

If we increase the amount of water (charge) in the right tank, we increase the pressure (voltage) on the water (charge) from gravitational forces (electromagnetic forces).
In turn, even though the hose is narrower (more resistance) on the right side than the left, we still see an equal amount of water flowing (current) out of the right pipe.
If we increased the amount of water (charge) in the left tank, we increase the pressure (voltage), which increases the amount of water flowing (current) through the left pipe.

- Water = Charge (measured in Coulombs)
- Pressure = Voltage (measured in Volts)
- Flow = Current (measured in Amperes, or "Amps" for short)
- Hose Width = Resistance (measured in Ohms)

As explained by the analogy, Ohm combined the elements of voltage, current, and resistance to develop the formula of Ohm's Law: `V = IR`. <br>
`V` = Voltage in Volts, `I` = Current in Amps, and `R` = Resistance in Ohms.

# 2. Device Components

Before diving into circuits, it is helpful to understand the context of **device components** within **digital circuits**.
While most physical variables in the real world (voltage, frequency, or position) are continuous (analog), digital systems abstract this information into discrete-valued variables.
Specifically, electronic computers generally use a binary representation, where a high enough voltage indicates a `1 (TRUE)` and a low enough voltage indicates a `0 (FALSE)`.

This digital abstraction allows designers to focus on the logical manipulation of 1s and 0s without constantly solving complex physics equations describing the motion of electrons in every component.
Digital circuits are the physical implementations of this logic, restricting voltages to discrete ranges to represent binary states.

## CMOS Transistors

Modern digital circuits are primarily built using **transistors**, which act as electronically controlled switches that turn ON and OFF when voltage or current is applied to a control terminal.
The two main types of transistors are *bipolar transistors* and *metal-oxide-semiconductor field effect transistors* (MOSFETs or MOS transistors, pronounced "moss-fets" or "M-O-S", respectively).
The specific technology used for the vast majority of chips today is known as CMOS (Complementary MOS).
To understand how these switches work, we must look at the underlying materials and components: semiconductors, diodes, and capacitors.

### Semiconductors

![conductivity](https://i.imgur.com/Et6rtVd.png)

An atom contains a nucleus of protons, surrounded by several orbital shells that contain a maximum amount of electrons.
The outermost orbital shell called the valence shell holds electrons with the most energy.
The electrons are held in place by the nucleus, however there's another shell called the conduction band.
If an electron can reach it, it can break free from the valence shell and move to another atom.
With a metal conductor like copper, the conduction band and valence shell overlap so it is very easy for the electron in the valence shell to move around freely.
Insulators, have a valence shell which is packed and the conduction band is too far away to conduct electricity.
In **semiconductors**, there is one too many electrons in the valence shell (4 electrons) so they act as insulators.
But since the conduction band is close, if we provide some external energy, some electrons can gain enough energy to reach the conduction band and break free of the atom.

Basically, a semiconductor materials ability to conduct electricity can be precisely controlled by adding impurities (doping) or applying voltage, light, or heat.
These semiconductor materials form the basis for transistors, diodes, and microchips that power modern electronics.

CMOS technology relies on Silicon (Si), a group IV atom (so it has four electrons in its valence shell and forms bonds with four adjacent atoms) that forms a crystalline lattice.
Pure silicon turns out to be a poor conductor, so engineers add impurities called **dopants** to alter its conductivity.
Adding Arsenic (group V) creates **n-type** silicon, which has free negatively charged electrons that act like negative charge carriers.
Adding Boron (group III) creates **p-type** silicon, which has "holes" (missing electrons) that act like positive charge carriers.

![semiconductors](https://i.imgur.com/1qnjdDw.png)

### Diodes

A **diode** is a semiconductor device, typically made of doped silicon, that essentially acts as a one-way switch for current.
It allows current to flow easily in one direction but severely restricts current from flowing in the opposite direction.

I want to go on a slight tangent here real fast and explain the types of current as it is relevant to diodes and transistors.
DC (Direct Current) flows steadily in one single direction (like from a battery), while AC (Alternating Current) periodically reverses direction, flowing back and forth in cycles (like wall outlets).
AC is ideal for power grids because its voltage can be easily changed with transformers for efficient long-distance transmission, while DC is used by most electronics and batteries, often requiring conversion from AC.
If you were curious, power grids use generators and transformers that rotate magnets to precisely control voltage levels that push electrons back and forth.
"But how exactly?" is beyond the scope of this study, and I will not be covering it here.

![currentdirection](https://i.imgur.com/fLfEv7w.png)

Back to topic. When n-type and p-type silicon are joined, they form a **diode**. A diode acts as a one-way valve for current.
The p-type region is called the anode and the n-type region is called the cathode.
When the voltage on the anode rises above the voltage on the cathode, the diode is forward biased, and current flows through the diode from the anode to the cathode.
But when the anode voltage is lower than the voltage on the cathode, the diode is reverse biased, and no current flows.

The moment you join p-type and n-type material, nature tries to reach an equilibrium through a process called **diffusion**.
Diffusion is simply the process of the high-concentration electrons from the n-type region rushing across the border to fill the "empty holes" in the p-type region.
When an electron meets a hole at the junction, they cancel each other out and stick in place.

On the n-side, you have atoms like Phosphorus with 5 valence electrons. Since they only need 4 electrons to bond, that 5th electron is free to roam.
However, the phosphorus atom is still electrically neutral because it has 15 protons and 15 electrons.
On the p-side, you have atoms like Boron with 3 valence electrons. They are also electrically neutral with 5 protons and 5 electrons, but they leave a "hole" in the lattice.

When the junction is formed, those tightly packed free electrons from the n-side jump across to fill the holes in the p-side.
As a result, the Phosphorus atom on the n-side just lost an electron making it a positive ion and the Boron atom on the p-side just gained an electron making it a negative ion.
Because these atoms are locked into the solid crystal lattice, they cannot move.
You are left with a layer of stationary positive charge near the junction on the n-side and a layer of stationary negative charge near the junction on the p-side.

![pnjunction](https://i.imgur.com/cWB9QSH.png)

This creates something called the **depletion region** at the PN junction, which contains no mobile charge carriers and only stationary charged ions.
In physics, whenever you have a separation of positive and negative charges that are fixed in space, an **electric field** is automatically created, and such is the case here.
These stationary ions near the junction create an internal electric field within the depletion region that acts like a wall, stopping any further electrons from crossing.
The internal electric field applies a force that repels negative charges from the n-side and repels positive charges from the p-side.
I know, the diagram above looks SO misleading and it honestly is extremely unintuitive.
The negative and positive symbols within the depletion region represent the charge of the ions, and the other symbols in the n-side and p-side represent free electrons and holes. Two very different things.
The electric field suggests that positive charges experience a force that pushes them towards the negatively charged p-side and negative charges experience a push towards the positively charged n-side.
That is what the diagram actually means.

Basically, this electric field creates a **potential barrier** which is simply the voltage equivalent of that field.
For electrons to cross the junction, a voltage bigger than the potential barrier needs to be applied.
Think of it like: the electric field is the steepness of the slope, and the voltage is the height of the hill.

You might be wondering: "why don't all the electrons just cross over until all holes are filled?"
Really, it's a balance of the two forces we talked about: diffusion and drift.
The natural tendency for electrons to cross over to fill the holes in the p-side (diffusion) and the repulsive force from the potential barrier (drift).
The depletion region stops growing the exact moment the electric field becomes strong enough to counteract the force of diffusion.
This state is known as equilibrium.

Before I dive into forward and reverse bias of a diode, I strongly recommend you to refresh your memory of the current intuition I explained earlier and really ingrain that pulling perspective of current.
When you apply a **forward bias** to a diode, you connect the positive terminal (high voltage) to the p-side and the negative terminal (or ground) to the n-side.
In turn, electrons are pulled away from the p-side (pushed into n-side), breaking the equilibrium, overcoming the voltage produced by the potential barrier, squashing the depletion region and allowing current to flow through.
However, when you apply a **reverse bias**, you connect the positive terminal (high voltage) to the n-side and the negative terminal (or ground) to the p-side.
This results in electrons being pulled away from the n-side junction, and in consequence pushes holes away from the p-side junction (widening the depletion region).
Since the free electrons (negative charge carriers) are pulled away from the junction, and empty holes (positive charge carriers) are pushed away from the junction, we are left with a wider depletion region at the junction of the diode filled with ions which strengthen the electric field and potential barrier even more.
So, a reverse biased diode acts as a strong insulator with very microscopic leakage of current.

Quick tangent to make sure you understand! In forward biased diodes, we can say "electrons are pulled from the p-side and pushed into the n-side of the diodes."
We can say this because current flows through diodes in forward bias, however, it is not the case for reverse biased diodes.
In reverse biased diodes, electrons feel a pulling force from the n-side which attract the electrons away from the junction.
This causes holes to be pushed away from the junction as well which causes the widening of the depletion region, blocking current.
However, there are no electrons being pushed into the p-side of the diode because the electron tug of war ends at the PN junction of the diode.
Revisit my notes on current intuition (find in table of contents) if you don't understand what I am trying to get at here.

All of that combined together should intuitively explain the exact science behind how diodes act as one-way valves for current.
Here is a quick [video](https://youtu.be/Fwj_d3uO5g8) to help visualize and understand the physics behind a diode.

Quick note! Diodes don't always allow current to flow in forward bias though.
A silicon diode requires a specific minimum voltage (known as the forward voltage drop ~ 0.6-1.0 V) to overcome its potential barrier before conducting electricity, after which current increases exponentially.
Even though diodes block current with reverse bias, if the reverse voltage is high enough (exceeding the diode's reverse breakdown voltage), it will conduct, but this usually causes permanent failure.

![diodes](https://i.imgur.com/RjCRjuf.png) <br>
*The diode symbol intuitively shows that current only flows in one direction.*

### Capacitors

A **capacitor** is an electrical circuit component that temporarily lets current flow through and temporarily stores electrical energy (like a battery).
It contains two conductive plates separated by an insulating dielectric.
A dielectric is an electrical insulator (glass, ceramic, plastic, etc) that supports an electrical field by becoming polarized, meaning its charges shift slightly but doesn't allow for current to flow.
This layer is essential, as it allows a voltage to develop across the plates by holding an electric charge instead of letting current flow between them.

In simple terms, the capacitance of a capacitor is the measure of capacitor's ability to store electrical charge onto its plates.
The ratio of stored charge `Q` to the applied voltage `V` gives the capacitance `C`: `C = Q / V`.
It is slightly unintuitive at first, but once you realize that charge and voltage are completely separate, capacitance starts to make more sense.
Think of it like: a bucket’s size (Capacitance) is independent of how much water (Charge) is in it or how much pressure (Voltage) is at the bottom.
When a voltage `V` is applied to one of the conductors, the conductor accumulates electric charge `Q` and the other conductor accumulates the opposite charge `-Q`.
While we often describe the charge as being held on the plates, the energy is more accurately stored in the electric field between them.
As current flows into the capacitor, the field strengthens, and as it discharges, the field weakens, releasing the stored energy back into the circuit.

Capacitance, measured in Farads (F), depends on several factors: the area of the conductive plates, the thickness and type of dielectric material, and the separation distance between the plates.
A larger plate area or smaller distance gap between them increases capacitance, allowing the capacitor to store more charge at a given voltage.
To show how these variables are related, you can also measure the capacitance of a capacitor using this formula: `C = 𝜀 * (A / d)`.
`𝜀` represents the permittivity (ability to store electrical energy in an electric field) of the dielectric material, `A` represents the area of the conductive plate, and `d` represents the distance between them.
1 Farad means the capacitor can hold 1 Coulomb of charge across a potential difference of 1 Volt.
You will more commonly see capacitors measured in pico-farads (pF), nano-farads (nF) or micro-farads (μF).

When a voltage is applied and electrons gather on a plate, the dielectric becomes positively charged near the negatively charged plate and vice versa. This process is called polarization.
The dielectric is influenced by the surrounding conductive plates to have a shift in its electron cloud which creates a tiny internal electric field.
The two oppositely charged conductive plates separated by the dielectric also begin to form a larger external electric field.
The dielectric not only helps as an insulator between the plates but also uses its internal field to oppose the external field of the plates.
It's important to note that this is an intended feature of the dielectric because it helps slow the growth of the opposing voltage from the external field, which in turn increases the capacitance of the capacitor.
The external electric field is strong enough to hold the charges in these plates until connected to another circuit to discharge the capacitor.

![capacitorcircuit](https://i.imgur.com/QF97Qta.png)

Before I begin explaining how charging and discharging a capacitor works, I want to explain how circuits actually work with capacitors since they are physically open circuits.
Both conductive plates within the capacitor have a bunch of electrons randomly roaming around much like the copper wire of any circuit.
Initially, when the capacitor is fully discharged, the plates are both electrically neutral and no energy or charge is stored yet.
Once you start charging the capacitor, electrons start to build up on one of the plates, drawing positive charge from the dielectric toward it and pushing the negative charge within the dielectric away.
This forms an electrical field around the capacitor which begins to push the electrons of the other plate out.
This creates the illusion of current "flowing through" the capacitor even though there are no electrons passing through the capacitor because of the insulator between the plates.
It is important to note that positive charges (protons) don't move since all the atoms are tethered in the solid dielectric, it is just the shifting electron clouds that create dipoles in the dielectric.

![rccircuit](https://i.imgur.com/LIfrOXz.png)

The circuit above contains a capacitor (`C`) in series with a resistor (`R`), both connected to a battery power supply (`V_s`) through a mechanical switch.
At the instant the switch is closed, the capacitor starts charging up through the resistor.
This charging process continues until the capacitor's voltage is equal to the battery supply's voltage.

![vcvstime](https://i.imgur.com/MUxUUPf.png)

As the capacitor starts charging, charge builds up on its plates, creating an increasing voltage `V_c` that opposes the battery voltage `V_s`.
This opposition reduces the current slowly as the voltage `V_c` approaches `V_s`, resulting in exponential decrease in current over time.

This charging behavior follows a time constant represented by: `𝜏 = RC`.
`R` represents the resistance of the circuit in Ohms, and `C` represents the capacitance of the circuit in Farads.
The time constant `𝜏` represents the time required for the capacitor to reach ~63% of its full charge potential.
The value of `𝜏` depends on the resistance `R` and capacitance `C`: a larger `R` slows the charging rate, while a larger `C` allows the capacitor to hold more charge, also requiring more time to reach full charge.

As time progresses, the voltage across the capacitor follows an exponential curve, increasing quickly at first but slowly as it approaches `V_s`.
At around `5𝜏`, the capacitor voltage `V_c` has essentially reached `V_s`, and we consider it fully charged.
At this point, known as the Steady State Period, the capacitor behaves like an open circuit, holding the fully supply of voltage across it, while current falls to 0, and the total charge reaches `Q = CV`.
The stored charge will forever stay in the capacitor and won't be lost until connected to another circuit. However, capacitors do leak charge in practice.
Note that theoretically, the capacitor never actually reaches 100% of its full charging potential.
Even after `5𝜏`, the capacitor only reaches 99.3%, but for all practical purposes, we can consider that capacitor fully charged at this point, as there is hardly any change after this.

![dischargingexample](https://i.imgur.com/8VtYd7e.png)

Now, take the circuit above with a capacitor and a bulb connected in parallel powered by a battery power supply through a mechanical switch.
When we close the switch, current flows through the circuit and charges up the capacitor and lights the bulb in parallel.
If we let the capacitor charge for a while and then open the switch, you can see that the bulb actually stays lit since the capacitor immediately starts discharging and releases its charge back into the circuit.
The bulb will stay lit until the capacitor is done discharging, meaning it is back to its default state and the plates have an equal charge again.
If we mimic a pulsating DC by repeatedly flipping the mechanical switch of the circuit, the bulb will stay lit all the time because it is being powered by the battery when the switch is closed and being powered by the capacitor when the switch is open.
This demonstrates how a capacitor can smoothen out the ripples that can appear while converting AC to DC.

Additionally, while a capacitor is placed in a DC circuit, it charges up to match the supply voltage, and once charged, it effectively blocks the flow of current.
In an AC circuit however, the capacitor behaves differently.
Since AC consistently changes direction, the capacitor repeatedly charges and discharges, creating an effect that lets AC current "pass through" the capacitor.

Here is a quick [video](https://youtu.be/X4EUwTwZ110) that visually explains how electricity "flows through" the capacitor.

### Current Rectification

Our homes are powered by power grids that provide an AC to our wall outlets.
And our electronic devices need to convert the AC from these outlets to DC because most sensitive electronics (computers, phones, etc.) run on a steady, one-way flow of electrons (DC), not the fluctuating AC waveform.
Our devices convert AC to DC using a process called **rectification** typically involving: a transformer to adjust the voltage, a rectifier circuit (diodes) to change AC to pulsating DC, a capacitor to smooth the ripples, and a voltage regulator to provide a steady, constant output for electronics.

This is a breakdown of all the steps in the rectification process:

1. **Step-Down Transformer**: The high AC voltage from the wall outlet is reduced to a lower, more manageable AC voltage level for the device.
2. **Rectifier (Diodes)**: Diodes allow current to flow in only one direction.
    - **Half-wave rectification**: Blocks the negative half of the AC wave, resulting in a pulsating DC.
    - **Full-wave rectification**: Uses four diodes to flip the negative half of the wave, making it positive, creating a smoother, but still bumpy, DC output.
3. **Filter (Capacitor)**: A capacitor charges up during the peaks of the pulsating DC and discharges during the dips, smoothing out the ripples and creating a steadier DC.
4. **Voltage Regulator**: The regulator ensures a precise, constant DC voltage by compensating for any remaining fluctuations, providing the stable power needed for sensitive electronics.

## nMOS and pMOS Transistors

MOSFETs are kind of like sandwiches that consist of layers of conductive and insulating materials. These MOSFETs are built on thin and flat **wafers** like most modern electronics.
A wafer is a thin slice of semiconductor material, typically high-purity crystalline silicon, used as the substrate for fabricating integrating circuits (chips) in electronics.
These thin, usually circular discs (15 - 30 cm in diameter) serve as the foundational base upon which microelectronic devices are manufactured through processes like doping, etching, and deposition.

The manufacturing process of a MOSFET obviously begins with a bare wafer, and then involves a sequence of steps in which dopants are implanted into the silicon, thin films of silicon dioxide and silicon are grown, and metal is deposited.
Between each step, the wafer is carefully and precisely patterned by very accurate and advanced laser technology so that the materials appear exactly where they are desired.
Since transistors are literally a fraction of a micron (1e-6 m) in length, an entire wafer is processed at once.
Once the processing is complete, the wafer is cut into tiny rectangles called **chips** containing millions or billions of transistors.
These chips are first tested, and then placed in a plastic or ceramic package with metal pins on the bottom to connect them to circuit boards.

<img src="https://i.imgur.com/mTtlJpJ.png" alt="irlwafer" width=400 />

Specifically, MOSFET sandwiches consist of 3 main layers: a conductive layer on the top called the gate, an insulating dielectric layer of silicon dioxide (`SiO_2`) in the middle, and the silicon wafer called the substrate on the bottom.
If you were wondering, silicon dioxide is basically just glass and also often simply called *oxide* in the semiconductor industry.
Historically, the gate was constructed from metal, hence the name metal-oxide-semiconductor, however, modern manufacturing processes use polycrystalline silicon for the gate because it doesn't melt during some of the following high-temperature processing steps.

![nmosandpmos](https://i.imgur.com/5bn2gNE.png)

As shown by the figure above, there are two flavors of MOSFETs: nMOS and pMOS. The figure illustrates the cross section of the nMOS and pMOS from the side.
The n-type transistors, also known as nMOS, have 2 separate regions of n-type dopants neighbouring the gate (called the **source** and **drain**) that were planted onto a p-type semiconductor substrate base.
The pMOS transistors are just the opposite, consisting of a p-type source and drain regions in an n-type substrate base.

Now you're probably wondering: "why are there 2 flavors of MOSFETs and what's the difference between how they function?"
Before I get into that, I want to first dive into the nMOS transistor and how the components we learned about earlier come together to operate this transistor.

<!-- TODO: fix opposing diodes logic that is entirely wrong -->
<!-- TODO: tiny correction of source and drain connectivity -->
The source and drain are both connected to a region of n-type dopant on top of the p-type substrate like shown in the diagram.
Doesn't this sound familiar? The source and drain are both connected to tiny diodes within the transistor that by default block the flow of current.
The PN junction from the n-type regions in the p-type substrate form a depletion region where some of the free electrons fill the holes in the p-type region and create a potential barrier.
Quick suggestion: maybe read up on diodes again to refresh your memory because it is pretty confusing and unintuitive.
This potential barrier in the source diode blocks current from flowing when theres no voltage, but what stops the current from flowing when there's a voltage applied to the source but not the gate?
Remember, we only want the transistor to pass current through when there is a voltage applied to the gate as well (our switch controller).
That's where the drain diode comes into play. Since the source diodes leak electrons into the p-type substrate, it only makes the potential barrier of the drain diode larger stopping current.
Long story short, it would be a forward bias for the source diode, but a reverse bias for the drain diode, therefore none of the current flows through.
Now that we realised both of the diodes are facing in opposite directions it seems impossible for current to pass through, but now I will explain how we use capacitors to make this work.

<!-- TODO: show image of nMOS operation, how the channel actually works -->
If you haven't noticed already, the metal-oxide-semiconductor sandwich we manufactured earlier actually forms a capacitor. Take a look at the figure of an nMOS transistor above.
There is a thin insulating dielectric layer (from the silicon dioxide) that separates the two conductive plates which are the polysilicon gate on top and the silicon wafer substrate on the bottom.
A MOSFET behaves as a voltage-controlled switch in which the gate voltage with the support of the dielectric creates an electric field that turns ON or OFF a connection between the source and drain, hence the name **field effect transistor**.
When you apply a small positive voltage to the gate, the dielectric creates an electric field that attracts electrons on the other side (wafer substrate).
The electric field allows the electrons to overcome the repulsion of the depletion regions of both diodes and creates a channel for electrons to flow through both diodes.
This channel is also known as the inversion layer because it temporarily inverts the top of the p-type substrate into an n-type region to allow the flow of electrons.
Long story short, the electric field created by the dielectric in the capacitor temporarily disables the potential barriers of the diodes allowing current to pass through freely.
Refer to the visual below or watch the [video](https://youtu.be/IcrBqCFLHIY) (where I grabbed it from) to really understand it more intuitively.

![fetdiagram](https://i.imgur.com/qhU9mNq.png)

<!-- TODO: what happens to the charge in the gate of the capacitor? REVISIT AFTER ALL OTHER FIXES -->
You might also be wondering: if the MOSFET uses the physical structure of a capacitor, does the gate also charge up when a positive voltage is applied and does it store the charge accumulated?
The answer is YES, the gate actually does start "charging" when a positive voltage is applied to it and stores the charge even when the voltage is disabled.
This brings up some problems because the transistor is considered ON as long as the electric field exists.
Meaning, even if the gate has no voltage applied to it, if it has stored charge keeping the electric field alive, the transistor is still allowing current to pass through.
To actually turn the transistor OFF, the circuit must provide a path for the electrons to leave the gate.
To solve this problem, the substrate of an nMOS transistor is normally tied to GND, the lowest voltage in the system.

<!-- TODO: talk about how pMOS is different from nMOS -->

<!-- TODO: rename note metadata, refactor introduction a bit, rename note titles, rename git branch, change everything to transistors instead of computer logic -->

---

# Resources

- [csl.cornell.edu/courses/ece2300](https://www.csl.cornell.edu/courses/ece2300/readings.html)
- "Digital Design and Computer Architecture, RISC-V Edition," by D. M. Harris and S. L. Harris (Morgan Kaufmann, 2021)
- [Making logic gates from transistors - YouTube](https://youtu.be/sTu3LwpF6XI)
- [learn.sparkfun.com (physics of electricity)](https://learn.sparkfun.com/tutorials/voltage-current-resistance-and-ohms-law/all)
- [fluke.com/blog/electrical/diode (what is a diode)](https://www.fluke.com/en-us/learn/blog/electrical/what-is-a-diode)
- [florisera.com/capacitors (what is a capacitor)](https://florisera.com/introduction-to-capacitors/)

---

*Written by BooleanCube :]*
