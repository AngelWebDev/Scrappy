**About arc42**

arc42, the Template for documentation of software and system
architecture.

By Dr. Gernot Starke, Dr. Peter Hruschka and contributors.

Template Revision: 7.0 EN (based on asciidoc), January 2017

© We acknowledge that this document uses material from the arc 42
architecture template, http://www.arc42.de. Created by Dr. Peter
Hruschka & Dr. Gernot Starke.

.. _section-introduction-and-goals:

Introduction and Goals
======================

The Scrappy Application will replace an existing windows application that is in use at one JunkYard.
The new application should be web based and cloud ready so we can sell it as a product to other JunkYard in a second step.

The application implements Use Cases supporting the arrival of scrap metal and other recyclable material.
It will record every arrival of material in the junkyard. For every arrival it will enable and document a payout at the cash desk.
All these transactions must be logged. At the end of each day a report will be generated for import into the main ERP system.

The technology should be web based so a common browser will suffice on the edge device.
The actual arrival will be entered on a tablet computer. Payout and Backoffice will be done on common PC hardware.
The server can be hosted inside the facility (on-premise). Later, the system will be extended to run in the cloud.

The software should be as simple as possible regarding UX and infrastructure requirements.

The users of the Software are:

- junk yard worker (arrival)
- office clerk (payout)
- management (backoffice)


.. __requirements_overview:

Requirements Overview
---------------------

**Backoffice App**
(will run on Office-PC)

- Manage Application users and Access Levels
-- (access to Arrival, Payout, Backoffice apps can be assigned)
- Manage Customers (Create, Search, Update)
- Generate Reports
- Browse through past payouts

**Arrival App**
(will run on tablet PC in Junk Yard environment)

- select customer (or "NEW customer")
- select Material
- enter weight
- Submit arrival

**Payout App**
(will run on Office-PC in office environment)

- view list of pending arrivals (not paid out yet)
- select one of these arrivals
- confirm Payout

- Browse past payouts (of current day)

.. __quality_goals:

Quality Goals
-------------

1. Simple and intuitive UX (especially for Arrival App)
2. Secure storage of arrival data (later enforced with external signature service)
3. Simple yet extendibe Software-Design

.. __stakeholders:

Stakeholders
------------

+-------------------+---------------------+------------------------------------------------------+
| Role/Name         | Contact             | Expectations                                         |
+===================+=====================+======================================================+
| *DevLead*         | *Gaylord Aulke*     | *Simple, Iterative Development*                      |
+-------------------+---------------------+------------------------------------------------------+
| *Product Owner*   | *Markus Schüler*    | *Understandible Code, Fast Progress to first version*|
+-------------------+---------------------+------------------------------------------------------+
| *Business Owner*  | *Marcus Aulfinger*  | *Time to market, Extendible Structure*               |
+-------------------+---------------------+------------------------------------------------------+

.. _section-architecture-constraints:

Architecture Constraints
========================

The system should have only few dependencies.
It should work on a normal office PC as client and server.
No separate database server.

The Client must work on tablets and Desktop PCs.

At a later stage, the system will be made multi-tennant capable and scaled to cloud level.
But this should not be considered in the first version.

.. _section-system-scope-and-context:

System Scope and Context
========================

**Contents.**

System scope and context - as the name suggests - delimits your system
(i.e. your scope) from all its communication partners (neighboring
systems and users, i.e. the context of your system). It thereby
specifies the external interfaces.

If necessary, differentiate the business context (domain specific inputs
and outputs) from the technical context (channels, protocols, hardware).

**Motivation.**

The domain interfaces and technical interfaces to communication partners
are among your system’s most critical aspects. Make sure that you
completely understand them.

**Form.**

Various options:

-  Context diagrams

-  Lists of communication partners and their interfaces.

.. __business_context:

Business Context
----------------

**Contents.**

Specification of **all** communication partners (users, IT-systems, …)
with explanations of domain specific inputs and outputs or interfaces.
Optionally you can add domain specific formats or communication
protocols.

**Motivation.**

All stakeholders should understand which data are exchanged with the
environment of the system.

**Form.**

All kinds of diagrams that show the system as a black box and specify
the domain interfaces to communication partners.

Alternatively (or additionally) you can use a table. The title of the
table is the name of your system, the three columns contain the name of
the communication partner, the inputs, and the outputs.

**<Diagram or Table>**

**<optionally: Explanation of external domain interfaces>**

.. __technical_context:

Technical Context
-----------------

**Contents.**

Technical interfaces (channels and transmission media) linking your
system to its environment. In addition a mapping of domain specific
input/output to the channels, i.e. an explanation with I/O uses which
channel.

**Motivation.**

Many stakeholders make architectural decision based on the technical
interfaces between the system and its context. Especially infrastructure
or hardware designers decide these technical interfaces.

**Form.**

E.g. UML deployment diagram describing channels to neighboring systems,
together with a mapping table showing the relationships between channels
and input/output.

**<Diagram or Table>**

**<optionally: Explanation of technical interfaces>**

**<Mapping Input/Output to Channels>**

.. _section-solution-strategy:

Solution Strategy
=================

**Contents.**

A short summary and explanation of the fundamental decisions and
solution strategies, that shape the system’s architecture. These include

-  technology decisions

-  decisions about the top-level decomposition of the system, e.g. usage
   of an architectural pattern or design pattern

-  decisions on how to achieve key quality goals

-  relevant organizational decisions, e.g. selecting a development
   process or delegating certain tasks to third parties.

**Motivation.**

These decisions form the cornerstones for your architecture. They are
the basis for many other detailed decisions or implementation rules.

**Form.**

Keep the explanation of these key decisions short.

Motivate what you have decided and why you decided that way, based upon
your problem statement, the quality goals and key constraints. Refer to
details in the following sections.

.. _section-building-block-view:

Building Block View
===================

**Content.**

The building block view shows the static decomposition of the system
into building blocks (modules, components, subsystems, classes,
interfaces, packages, libraries, frameworks, layers, partitions, tiers,
functions, macros, operations, datas structures, …) as well as their
dependencies (relationships, associations, …)

This view is mandatory for every architecture documentation. In analogy
to a house this is the *floor plan*.

**Motivation.**

Maintain an overview of your source code by making its structure
understandable through abstraction.

This allows you to communicate with your stakeholder on an abstract
level without disclosing implementation details.

**Form.**

The building block view is a hierarchical collection of black boxes and
white boxes (see figure below) and their descriptions.

|Hierarchy of building blocks|

**Level 1** is the white box description of the overall system together
with black box descriptions of all contained building blocks.

**Level 2** zooms into some building blocks of level 1. Thus it contains
the white box description of selected building blocks of level 1,
together with black box descriptions of their internal building blocks.

**Level 3** zooms into selected building blocks of level 2, and so on.

.. __whitebox_overall_system:

Whitebox Overall System
-----------------------

Here you describe the decomposition of the overall system using the
following white box template. It contains

-  an overview diagram

-  a motivation for the decomposition

-  black box descriptions of the contained building blocks. For these we
   offer you alternatives:

   -  use *one* table for a short and pragmatic overview of all
      contained building blocks and their interfaces

   -  use a list of black box descriptions of the building blocks
      according to the black box template (see below). Depending on your
      choice of tool this list could be sub-chapters (in text files),
      sub-pages (in a Wiki) or nested elements (in a modeling tool).

-  (optional:) important interfaces, that are not explained in the black
   box templates of a building block, but are very important for
   understanding the white box. Since there are so many ways to specify
   interfaces why do not provide a specific template for them. In the
   worst case you have to specify and describe syntax, semantics,
   protocols, error handling, restrictions, versions, qualities,
   necessary compatibilities and many things more. In the best case you
   will get away with examples or simple signatures.

**<Overview Diagram>**

Motivation
   *<text explanation>*

Contained Building Blocks
   *<Description of contained building block (black boxes)>*

Important Interfaces
   *<Description of important interfaces>*

Insert your explanations of black boxes from level 1:

If you use tabular form you will only describe your black boxes with
name and responsibility according to the following schema:

+-----------------------+-----------------------------------------------+
| **Name**              | **Responsibility**                            |
+=======================+===============================================+
| *<black box 1>*       |  *<Text>*                                     |
+-----------------------+-----------------------------------------------+
| *<black box 2>*       |  *<Text>*                                     |
+-----------------------+-----------------------------------------------+

If you use a list of black box descriptions then you fill in a separate
black box template for every important building block . Its headline is
the name of the black box.

.. ___name_black_box_1:

<Name black box 1>
~~~~~~~~~~~~~~~~~~

Here you describe <black box 1> according the the following black box
template:

-  Purpose/Responsibility

-  Interface(s), when they are not extracted as separate paragraphs.
   This interfaces may include qualities and performance
   characteristics.

-  (Optional) Quality-/Performance characteristics of the black box,
   e.g.availability, run time behavior, ….

-  (Optional) directory/file location

-  (Optional) Fulfilled requirements (if you need traceability to
   requirements).

-  (Optional) Open issues/problems/risks

*<Purpose/Responsibility>*

*<Interface(s)>*

*<(Optional) Quality/Performance Characteristics>*

*<(Optional) Directory/File Location>*

*<(Optional) Fulfilled Requirements>*

*<(optional) Open Issues/Problems/Risks>*

.. ___name_black_box_2:

<Name black box 2>
~~~~~~~~~~~~~~~~~~

*<black box template>*

.. ___name_black_box_n:

<Name black box n>
~~~~~~~~~~~~~~~~~~

*<black box template>*

.. ___name_interface_1:

<Name interface 1>
~~~~~~~~~~~~~~~~~~

…

.. ___name_interface_m:

<Name interface m>
~~~~~~~~~~~~~~~~~~

.. __level_2:

Level 2
-------

Here you can specify the inner structure of (some) building blocks from
level 1 as white boxes.

You have to decide which building blocks of your system are important
enough to justify such a detailed description. Please prefer relevance
over completeness. Specify important, surprising, risky, complex or
volatile building blocks. Leave out normal, simple, boring or
standardized parts of your system

.. __white_box_emphasis_building_block_1_emphasis:

White Box *<building block 1>*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

…describes the internal structure of *building block 1*.

*<white box template>*

.. __white_box_emphasis_building_block_2_emphasis:

White Box *<building block 2>*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*<white box template>*

…

.. __white_box_emphasis_building_block_m_emphasis:

White Box *<building block m>*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*<white box template>*

.. __level_3:

Level 3
-------

Here you can specify the inner structure of (some) building blocks from
level 2 as white boxes.

When you need more detailed levels of your architecture please copy this
part of arc42 for additional levels.

.. __white_box_building_block_x_1:

White Box <_building block x.1_>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Specifies the internal structure of *building block x.1*.

*<white box template>*

.. __white_box_building_block_x_2:

White Box <_building block x.2_>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*<white box template>*

.. __white_box_building_block_y_1:

White Box <_building block y.1_>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*<white box template>*

.. _section-runtime-view:

Runtime View
============

**Contents.**

The runtime view describes concrete behavior and interactions of the
system’s building blocks in form of scenarios from the following areas:

-  important use cases or features: how do building blocks execute them?

-  interactions at critical external interfaces: how do building blocks
   cooperate with users and neighboring systems?

-  operation and administration: launch, start-up, stop

-  error and exception scenarios

Remark: The main criterion for the choice of possible scenarios
(sequences, workflows) is their **architectural relevance**. It is
**not** important to describe a large number of scenarios. You should
rather document a representative selection.

**Motivation.**

You should understand how (instances of) building blocks of your system
perform their job and communicate at runtime. You will mainly capture
scenarios in your documentation to communicate your architecture to
stakeholders that are less willing or able to read and understand the
static models (building block view, deployment view).

**Form.**

There are many notations for describing scenarios, e.g.

-  numbered list of steps (in natural language)

-  activity diagrams or flow charts

-  sequence diagrams

-  BPMN or EPCs (event process chains)

-  state machines

-  …

.. ___runtime_scenario_1:

<Runtime Scenario 1>
--------------------

-  *<insert runtime diagram or textual description of the scenario>*

-  *<insert description of the notable aspects of the interactions
   between the building block instances depicted in this diagram.>*

.. ___runtime_scenario_2:

<Runtime Scenario 2>
--------------------

.. __:

…
-

.. ___runtime_scenario_n:

<Runtime Scenario n>
--------------------

.. _section-deployment-view:

Deployment View
===============

**Content.**

The deployment view describes:

1. the technical infrastructure used to execute your system, with
   infrastructure elements like geographical locations, environments,
   computers, processors, channels and net topologies as well as other
   infrastructure elements and

2. the mapping of (software) building blocks to that infrastructure
   elements.

Often systems are executed in different environments, e.g. development
environment, test environment, production environment. In such cases you
should document all relevant environments.

Especially document the deployment view when your software is executed
as distributed system with more then one computer, processor, server or
container or when you design and construct your own hardware processors
and chips.

From a software perspective it is sufficient to capture those elements
of the infrastructure that are needed to show the deployment of your
building blocks. Hardware architects can go beyond that and describe the
infrastructure to any level of detail they need to capture.

**Motivation.**

Software does not run without hardware. This underlying infrastructure
can and will influence your system and/or some cross-cutting concepts.
Therefore, you need to know the infrastructure.

Maybe the highest level deployment diagram is already contained in
section 3.2. as technical context with your own infrastructure as ONE
black box. In this section you will zoom into this black box using
additional deployment diagrams:

-  UML offers deployment diagrams to express that view. Use it, probably
   with nested diagrams, when your infrastructure is more complex.

-  When your (hardware) stakeholders prefer other kinds of diagrams
   rather than the deployment diagram, let them use any kind that is
   able to show nodes and channels of the infrastructure.

.. __infrastructure_level_1:

Infrastructure Level 1
----------------------

Describe (usually in a combination of diagrams, tables, and text):

-  the distribution of your system to multiple locations, environments,
   computers, processors, .. as well as the physical connections between
   them

-  important justification or motivation for this deployment structure

-  Quality and/or performance features of the infrastructure

-  the mapping of software artifacts to elements of the infrastructure

For multiple environments or alternative deployments please copy that
section of arc42 for all relevant environments.

**<Overview Diagram>**

Motivation
   *<explanation in text form>*

Quality and/or Performance Features
   *<explanation in text form>*

Mapping of Building Blocks to Infrastructure
   *<description of the mapping>*

.. __infrastructure_level_2:

Infrastructure Level 2
----------------------

Here you can include the internal structure of (some) infrastructure
elements from level 1.

Please copy the structure from level 1 for each selected element.

.. ___emphasis_infrastructure_element_1_emphasis:

*<Infrastructure Element 1>*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*<diagram + explanation>*

.. ___emphasis_infrastructure_element_2_emphasis:

*<Infrastructure Element 2>*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*<diagram + explanation>*

…

.. ___emphasis_infrastructure_element_n_emphasis:

*<Infrastructure Element n>*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*<diagram + explanation>*

.. _section-concepts:

Cross-cutting Concepts
======================

**Content.**

This section describes overall, principal regulations and solution ideas
that are relevant in multiple parts (= cross-cutting) of your system.
Such concepts are often related to multiple building blocks. They can
include many different topics, such as

-  domain models

-  architecture patterns or design patterns

-  rules for using specific technology

-  principal, often technical decisions of overall decisions

-  implementation rules

**Motivation.**

Concepts form the basis for *conceptual integrity* (consistency,
homogeneity) of the architecture. Thus, they are an important
contribution to achieve inner qualities of your system.

Some of these concepts cannot be assigned to individual building blocks
(e.g. security or safety). This is the place in the template that we
provided for a cohesive specification of such concepts.

**Form.**

The form can be varied:

-  concept papers with any kind of structure

-  cross-cutting model excerpts or scenarios using notations of the
   architecture views

-  sample implementations, especially for technical concepts

-  reference to typical usage of standard frameworks (e.g. using
   Hibernate for object/relational mapping)

**Structure.**

A potential (but not mandatory) structure for this section could be:

-  Domain concepts

-  User Experience concepts (UX)

-  Safety and security concepts

-  Architecture and design patterns

-  "Under-the-hood"

-  development concepts

-  operational concepts

Note: it might be difficult to assign individual concepts to one
specific topic on this list.

|Possible topics for crosscutting concepts|

.. ___emphasis_concept_1_emphasis:

*<Concept 1>*
-------------

*<explanation>*

.. ___emphasis_concept_2_emphasis:

*<Concept 2>*
-------------

*<explanation>*

…

.. ___emphasis_concept_n_emphasis:

*<Concept n>*
-------------

*<explanation>*

.. _section-design-decisions:

Design Decisions
================

**Contents.**

Important, expensive, large scale or risky architecture decisions
including rationals. With "decisions" we mean selecting one alternative
based on given criteria.

Please use your judgement to decide whether an architectural decision
should be documented here in this central section or whether you better
document it locally (e.g. within the white box template of one building
block).

Avoid redundancy. Refer to section 4, where you already captured the
most important decisions of your architecture.

**Motivation.**

Stakeholders of your system should be able to comprehend and retrace
your decisions.

**Form.**

Various options:

-  List or table, ordered by importance and consequences or:

-  more detailed in form of separate sections per decision

-  ADR (architecture decision record) for every important decision

.. _section-quality-scenarios:

Quality Requirements
====================

**Content.**

This section contains all quality requirements as quality tree with
scenarios. The most important ones have already been described in
section 1.2. (quality goals)

Here you can also capture quality requirements with lesser priority,
which will not create high risks when they are not fully achieved.

**Motivation.**

Since quality requirements will have a lot of influence on architectural
decisions you should know for every stakeholder what is really important
to them, concrete and measurable.

.. __quality_tree:

Quality Tree
------------

**Content.**

The quality tree (as defined in ATAM – Architecture Tradeoff Analysis
Method) with quality/evaluation scenarios as leafs.

**Motivation.**

The tree structure with priorities provides an overview for a sometimes
large number of quality requirements.

**Form.**

The quality tree is a high-level overview of the quality goals and
requirements:

-  tree-like refinement of the term "quality". Use "quality" or
   "usefulness" as a root

-  a mind map with quality categories as main branches

In any case the tree should include links to the scenarios of the
following section.

.. __quality_scenarios:

Quality Scenarios
-----------------

**Contents.**

Concretization of (sometimes vague or implicit) quality requirements
using (quality) scenarios.

These scenarios describe what should happen when a stimulus arrives at
the system.

For architects, two kinds of scenarios are important:

-  Usage scenarios (also called application scenarios or use case
   scenarios) describe the system’s runtime reaction to a certain
   stimulus. This also includes scenarios that describe the system’s
   efficiency or performance. Example: The system reacts to a user’s
   request within one second.

-  Change scenarios describe a modification of the system or of its
   immediate environment. Example: Additional functionality is
   implemented or requirements for a quality attribute change.

**Motivation.**

Scenarios make quality requirements concrete and allow to more easily
measure or decide whether they are fulfilled.

Especially when you want to assess your architecture using methods like
ATAM you need to describe your quality goals (from section 1.2) more
precisely down to a level of scenarios that can be discussed and
evaluated.

**Form.**

Tabular or free form text.

.. _section-technical-risks:

Risks and Technical Debts
=========================

**Contents.**

A list of identified technical risks or technical debts, ordered by
priority

**Motivation.**

“Risk management is project management for grown-ups” (Tim Lister,
Atlantic Systems Guild.)

This should be your motto for systematic detection and evaluation of
risks and technical debts in the architecture, which will be needed by
management stakeholders (e.g. project managers, product owners) as part
of the overall risk analysis and measurement planning.

**Form.**

List of risks and/or technical debts, probably including suggested
measures to minimize, mitigate or avoid risks or reduce technical debts.

.. _section-glossary:

Glossary
========

**Contents.**

The most important domain and technical terms that your stakeholders use
when discussing the system.

You can also see the glossary as source for translations if you work in
multi-language teams.

**Motivation.**

You should clearly define your terms, so that all stakeholders

-  have an identical understanding of these terms

-  do not use synonyms and homonyms

**Form.**

A table with columns <Term> and <Definition>.

Potentially more columns in case you need translations.

+-----------------------------------+-----------------------------------+
| Term                              | Definition                        |
+===================================+===================================+
| <Term-1>                          | <definition-1>                    |
+-----------------------------------+-----------------------------------+
| <Term-2>                          | <definition-2>                    |
+-----------------------------------+-----------------------------------+

.. |arc42| image:: images/arc42-logo.png
.. |Hierarchy of building blocks| image:: images/05_building_blocks-EN.png
.. |Possible topics for crosscutting concepts| image:: images/08-Crosscutting-Concepts-Structure-EN.png

