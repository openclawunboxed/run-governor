# quickstart

## 1 install the governor

copy the `governor` directory into your project.

## 2 configure limits

set basic limits:

- max steps
- max cost
- duplicate tool call threshold

## 3 classify tools

create a tool risk matrix:

read only  
internal write  
external write  

## 4 enable tracing

log each step of the run using the provided trace schema.

## 5 run your first governed workflow

wrap your workflow execution with the run governor.

this allows the governor to intercept every step.
