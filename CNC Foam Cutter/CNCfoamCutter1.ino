#include <AccelStepper.h>

// Define stepper driver type (1 = driver with STEP+DIR)
#define MOTOR_INTERFACE_TYPE 1

// Pin definitions
#define A1x1 1
#define A2x1 2
#define B1x1 3
#define B2x1 4
#define A1y1 5
#define A2y1 6
#define B1y1 7
#define B2y1 8
#define A1y2 9
#define A2y2 10
#define B1y2 11
#define B2y2 12

// Create stepper objects
// below format works for TB6612 (Bipolar, constant voltage, H-Bridge motor driver)
AccelStepper stepperX1(AccelStepper::FULL4WIRE, A1x1, A2x1, B1x1, B2x1);
AccelStepper stepperY1(AccelStepper::FULL4WIRE, A1y1, A2y1, B1y1, B2y1);
AccelStepper stepperY2(AccelStepper::FULL4WIRE, A1y2, A2y2, B1y2, B2y2);

// Example airfoil path (simple shape for demo)
const int numPoints = 6;
float path[numPoints][2] = {
  {0, 0},
  {50, 10},
  {100, 0},
  {100, -10},
  {50, -5},
  {0, 0}
};

// Conversion factor: mm → steps
float stepsPerMM = 80.0;

// Track current target
int currentPoint = 0;

void setup() {
  Serial.begin(115200);

  stepperX1.setMaxSpeed(800);
  stepperX1.setAcceleration(400);

  stepperY1.setMaxSpeed(800);
  stepperY1.setAcceleration(400);

  Serial.println("Hot Wire Cutter Ready");
}

void loop() {
  if (currentPoint < numPoints) {
    moveToPoint(path[currentPoint][0], path[currentPoint][1]);
    currentPoint++;
    delay(200); // small pause between moves
  }
}

// Function to move both axes together
void moveToPoint(float x_mm, float y_mm) {
  long x_steps = x_mm * stepsPerMM;
  long y_steps = y_mm * stepsPerMM;

  stepperX1.moveTo(x_steps);
  stepperY1.moveTo(y_steps);
  stepperY2.moveTo(y_steps);

  while (stepperX1.distanceToGo() != 0 || stepperY1.distanceToGo() != 0) {
    stepperX1.run();
    stepperY1.run();
    stepperY2.run();
  }

  Serial.print("Moved to: ");
  Serial.print(x_mm);
  Serial.print(", ");
  Serial.println(y_mm);
}
