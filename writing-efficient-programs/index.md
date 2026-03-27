Writing efficient programs has turned into an art of its own these days, but it wasn't always like this.
In the early days of computing, programmers needed to fully understand the inner workings of a processor to be able to program it.
Back then, the efficiency of your program didn't matter because there weren't many ways to solve the same problem.
As the processor hardware got better, so did the performance of these programs, and therefore programmers of this era got "free" performance upgrades and didn't need to optimize their programs often.
However, things changed in 2005 when the typical power processors required plateaued.
Once we maxed out the amount of power we could provide to processors without frying them, the hardware couldn't get much faster.
Lower power supply means lower voltages provided to charge/discharge the transistors inside the processor, slowing it down significantly.

Even though hardware advancements might have slowed down, performance upgrade demands will forever stay.
So now, instead of making a single processor faster, hardware designers began packing multiple cores onto the same die and introduced advanced, complex processor enhancements.
Consequently, great performance no longer "just happens" and programmers need to actively design their code to utilize concurrency efficiently and understand the intricacies of hardware and compilers.

# Introduction to Performance and Concurrency

Every year, the most powerful computers, equipped with the ever-growing number of
the latest, most powerful processors, running the latest software versions (optimized to
leverage increasingly more processors and to use each one more efficiently), do the work
needed to build the next year's most powerful computers, and every year, this task is
balanced on the edge of what is barely possible. That we do not fall off this edge is largely
the achievement of the hardware and the software engineers, as the former supply the
growing compute power, and the latter use it with maximum efficiency.

## What is performance?

While efficiency is *related* to performance, it is not exactly the same.
Efficiency deals with using resources and wasting them as less as possible. An efficient program makes good use of computational hardware.

On the one hand, efficient programs don't leave available resources idle.
For example, if you have a computation that needs to be done and a processor sitting idle, that processor should handle the computation immediately.
Processors these days have many computing resources in them, and efficient programs try to make use of as many of these resources as possible at the same time.
But also, an efficient program doesn't waste resources with unnecessary computations like wasting memory space with data that is never used.

Performance, on the other hand, always relates to some metrics and the most common one is program "speed".
The better way to define this metric is **throughput**, which is the amount of computation a program does in a given period of time.
And the inverse metric for throughput, that is more commonly used for the same purpose, is the **turnaround time**, which is the amount of time required to compute a particular result.

However, that is not the only possible definition of performance.

### Performance as throughput

<div align="center">
  <img src="https://i.imgur.com/6eLluSM.png" alt="Performance as throughput" />
  <p><em>Figure 1.1: Run times of four different implementations of the same algorithm (relative units)</em></p>
</div>

Let's consider four programs that use different implementations to compute the same end result. The units of the performance are irrelevant in this case since we're interested in the relative performance.

It seems obvious that Program B has the highest performance because the turnaround time says it finished before the other three programs.
In many situations, this would be all the data we need to choose the best implementation for our problem.

But the context of the problem also matters.
Not only that, but these programs are also being run on battery-powered devices such as cellphones or laptops, and therefore the power consumption matters as well.

### Performance as power consumption

<div align="center">
  <img src="https://i.imgur.com/gR9bVrX.png" alt="Performance as power consumption" />
  <p><em>Figure 1.2: Power consumption of four different implementations of the same algorithm (relative units)</em></p>
</div>

This time, let's look at the power consumption of each of these four programs during the course of the computation.
From the data above, we can see that despite taking longer, Program C consumed less power overall.
So which program has the best performance?

It's still a tricky question to answer though because we still don't have the full context of the problem.
The program not only runs on a battery-powered device, but it also performs a real-time computation (e.g. it is used in audio processing).
It may seem that in this particular scenario we should prioritize speed but that is not the case.

### Performance for real-time applications

<div align="center">
  <img src="https://i.imgur.com/inVgiMr.png" alt="Performance for real-time applications" />
  <p><em>Figure 1.3: 95% latency of four different implementations of the same algorithm (percents)</em></p>
</div>

A real-time program must keep up with the events it is processing at all times.
An audio processor must keep up with speech, in particular.
If the program can process audio ten times faster than a person can speak, it does us no good, and we may as well turn our attention to power consumption.

On the other hand, if the program occasionally falls behind, some sounds or even words will be dropped.
This suggests that the real time, or speed, matters up to a point, but it must be delivered in a predictable manner.
