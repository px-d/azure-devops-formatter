Feature: Example

  Background:
    Given an innocent step in background

  Scenario: First scenario
    Given this steps outputs "hello"
    When this step fails
    Then not reached here