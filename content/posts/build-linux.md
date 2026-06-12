---
title: "Build my own Linux?"
date: "2026-06-12 17:23"
description: "After years of thinking about it, I'm finally exploring what it takes to build a minimal Linux system from the ground up."
tag: tech, linux
---

# Build my own Linux?

I've been using Linux for almost 15 years now, and for a very long time I've had the idea of building my own distro.

Well, maybe not a full distro.

At least a minimal bootable Linux system.

I've been thinking about it for months.

Actually, that's not true.

Years.

So I finally started digging into how Linux systems are put together, and honestly, it seems surprisingly simple once you strip away all the abstractions.

Most of us nerds already know this, but Linux itself is just the kernel.

The kernel talks to the hardware and provides the interface that applications, services, and userspace tools rely on.

The rest is userspace.

A root filesystem, a bunch of directories, configuration files, permissions, libraries, and programs glued together into something usable.

When you look at it that way, it suddenly feels a lot less magical.

Two tools that caught my attention are:

`pacstrap` can bootstrap a minimal Arch system into a directory, while 
`debootstrap` does roughly the same thing for Debian-based systems.

Both seem like excellent starting points if the goal is to understand what is actually required to get a Linux system up and running.

The more I read about it, the more tempting the idea becomes.

Maybe it's finally time to stop thinking about it and actually build something.

Oh, btw.

Cheers, it's Friday. 🍺
