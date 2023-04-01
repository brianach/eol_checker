![Alt text](media/vt100.jpg)

# EOL Checker

### Introduction

EOL Checker is a small program which simulates an IT hardware inventory for a 5 year old company of 50 employees. You log in as the administrator and from there you can view and sscroll through the inventory. You have the option to update any hardware that has reached its end of life cycle.

## Detailed Description

Most of the magic in this program happens under the hood as is usually the case and there are three main aspects to the program.

* Simulation

    The inventory simulation is calculated over a 5 year cylce. 10 random dates are generated for
    the each year and these are ordered in sequence with the first date at the top of the sequence. Then each date is prefixed with a capital letter which is the first letter of the hardware type followed by a 3 digit zero prefixed number.

    In order to simulate a real world scenario the hardware is given an average failure rate and this is simulated by generating a random number between 1 - 3 for the 10 items in each hardware list for the given year. A separate random number is generated for each hardware type. Having generated the random number, a random selection equal to that hardware type's random number is then removed from the list. Finally a new random date which must be later than the removed item's date is generated. A new item is created, again using the capitalised first letter of the hardware type followed by 3 digit zero prefixed ID incremented from the id of the last item in the corresponding hardware type list and the newly created random date is added to the end of the item. This is then appended to the corresponding hardware type list.

    To add another layer of complexity, again simulating a real world type scenario, each hardware type is given an end of life (EOL) value. After the first year has been generated and another year added using the same process as above, each hardware type is checked against its corresponding EOL value. If any of the items in the hardware type lists match this EOL value, then they are removed and a new set or list of items are appended using the same nomenclature as before.

    When the cycle of 5 years is completed the inventory is sent to a google sheet. At this point the columns will each have a heading listing the hardware type, followed by 50 rows of items. The item names will generally follow in order by descending dates and id numbers, but we should see gaps and random changes from the real world type simulation method by which the inventory was generated. Also many changes will be observed for some hardware types which have a short EOL but less so for hardware types with a longer EOL.

* Presentation

    The presentation of the program harks back to the mid to late 20th century heyday of minicomputers and mainframes which used crt terminals which were limited to little more than 2 colours. The look and feel is similiar to something like the VAX or PDP from Digital. Given more time I would have loved to emulate these in a way which would be more true to the original. This will be the plan for a next version.

* Interaction

    There isn't much going on here as most of the magic happens in the simulation but there is some code of very minor complexity used to generate the color palette and the layout. Ideally the screen would be made up of separate areas which would be changed independently of the screen header and footer but it was not possible for me to do this here. Due to this the screen is regenerated in its entirety each time the user chooses an option. Luckily due to the processing power of today's computers this doesn't present an issue and if anything serves to mimic the screen refresing abilities of older 20th century hardware. 

## Bugs

* EOL Hardware screen and menu options are problematic but don't prevent the program from running or cause the program to crash. Unforunately it was impossible to troubleshoot using the Gitpod debugger becuase the readchar module causes the debugger to crash. This will need to be manually debugged which was not possible at this point due to time constraints.

## Unimplemented Features

* The Exit Inventory opotion on the main screen menu does not do anything. Although it is coded to break out of the loop this doesn't happen. Again it was impossible to troubleshoot using the Gitpod debugger becuase the readchar module causes the debugger to crash. This will need to be manually debugged which was not possible at this point due to time constraints.
