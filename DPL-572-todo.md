# DPL-572 TODO

- Check with Scott if the Lysate Event creation to the Event WH is still required.

If Event message required:
- Create mapping of user/ robot/ barcode/ control locations to the event warehouse structure: subject type/ role type etc. See Event WH confluence links in story for help. (e.g. user/ robot/ barcode/ control_locations are each a subject)
- Add event type to Events WH repo and create/ update confluence documents. with description for DB. Run migration on deployment
- After sucessfully parsing Sequencescape's response, create the message to send to the Events WH (`lighthouse/classes/messages/warehouse_messages.py` might be useful - see how other events are created in the code for possible reuse)
- Send the `lystate_creation_event' to Events WH with data: user/ robot/ barcode/ control locations

- Go through `TODO (DPL-572)`'s (mostly all optional refactoring)
- Test `tests/routes/v1/test_pickings.py` (This is In Progress, but will be currently failing.)
- Test `tests/helpers/test_plates_helpers.py`
- Integration Suite (Ask Andrew for help)
- Run Linters (flake8 etc)
