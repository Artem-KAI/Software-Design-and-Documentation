# 🧪 Laboratory Work 1
## Designing a Messaging System

## 🔹 Variant 1 — Basic One-to-One Messaging
**Focus:** basic system architecture

**Requirements:**
- One user sends messages to another user
- No group chats
- Online and offline users supported

**Key questions:**
- Where are messages stored?
- How is delivery guaranteed?

---

## Part 1 — Component Diagram (30%)

### Task 
Show system components, their responsibilities, and interactions.
### Components
- Client (Web / Mobile)
- Backend API
- Authentication Service
- Message Service
- Database
- Delivery Mechanism (Queue / WebSocket / Push Service)

graph LR
  Client --> API
  API --> AuthService
  API --> MessageService
  MessageService --> DB[(Messages DB)]
  MessageService --> Queue
  Queue --> DeliveryService
  DeliveryService --> Client

---

## Part 2 — Sequence Diagram (25%)

### Scenario
- User A sends a message to user B who is offline.
  
sequenceDiagram
  participant A as User A
  participant Client
  participant API
  participant Msg as Message Service
  participant DB
  participant Queue
  participant Delivery

  A->>Client: Send message
  Client->>API: POST /messages
  API->>Msg: createMessage()
  Msg->>DB: save(message)
  Msg->>Queue: enqueue delivery
  API-->>Client: 202 Accepted
  Queue->>Delivery: attempt delivery
  Delivery-->>Client B: deliver when online

---

## Part 3 — State Diagram (20%)

### Object
- Message
### Task
- Describe the message lifecycle.

stateDiagram-v2
  [*] --> Created
  Created --> Sent
  Sent --> Delivered
  Delivered --> Read
  Sent --> Failed
  Failed --> Retried
  Retried --> Sent

---

## Part 4 — RFC (Request for Comments) (15%)

### Topic
- Message delivery strategy for online and offline users

# RFC: Message Delivery Strategy

## Context
Users can be online or offline when messages are sent.

## Problem
Messages must not be lost and delivery status must be reliable.

## Proposed Solution
Use asynchronous delivery with a message queue and client acknowledgements.

## Alternatives
- Direct delivery only (rejected)
- Client polling (considered)

## Consequences
+ Reliable delivery
- Higher infrastructure complexity

---

## Part 5 — ADR (Architecture Decision Record) (10%)

### Architecture Decision

# ADR-001: Use Message Queue for Delivery

## Status
Accepted

## Decision
Message delivery will be handled asynchronously using a queue.

## Consequences
- Messages survive client disconnects
- Delivery reliability improved
- Additional infrastructure required
