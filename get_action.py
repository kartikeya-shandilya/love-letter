#!/usr/bin/env python


def get_action(dropper,
               A,
               B,
               CARDS,
               drop,
               hmaid_flag,
               A_knows,
               B_knows,
               win_flag=None):
    """ Function to get outcome of a card-drop """
    # assign actor, other
    actor = A[:]
    other = B[:]
    if dropper == 'B':
        actor = B[:]
        other = A[:]
    new_drop = None

    # if card drop is Guard, take the guess and check if right?
    if drop in range(12, 19):
        if other[0] == drop % 10 and not hmaid_flag:
            win_flag = dropper
    # if priest then see the other person's card.. #TODO-ignoring now..
    elif drop == 2:
        pass
    # if baron, compare hands and assign winner whoever is bigger
    elif drop == 3 and not hmaid_flag:
        if A[0] > B[0]: win_flag = "A"
        elif B[0] > A[0]: win_flag = "B"
        else: win_flag = "Draw"
    # if housemaid, dropper is protected for next hand
    elif drop == 4:
        pass
    # if prince, decide based on drop actor / drop other..
    elif drop in range(50, 52):
        if drop == 50:
            new_drop = actor.pop(0)
            if dropper == "A" and new_drop == B_knows:
                B_knows = 0
            if dropper == "B" and new_drop == A_knows:
                A_knows = 0
            if new_drop == 8:
                win_flag = ["A", "B"][dropper == "A"]
            actor.append(CARDS.pop(0))
        elif drop == 51 and not hmaid_flag:
            new_drop = other.pop(0)
            if dropper == "A" and new_drop == B_knows:
                B_knows = 0
            if dropper == "B" and new_drop == A_knows:
                A_knows = 0
            if new_drop == 8:
                win_flag == dropper
            other.append(CARDS.pop(0))
        A = actor[:]
        B = other[:]
        if dropper == 'B':
            A = other[:]
            B = actor[:]
    # if king, exchange hands
    elif drop == 6 and not hmaid_flag:
        temp = actor[:]
        actor = other[:]
        other = temp[:]
        A = actor[:]
        B = other[:]
        if dropper == 'B':
            A = other[:]
            B = actor[:]
    # if countess, nothing..
    elif drop == 7:
        pass
    # if princess, lose
    elif drop == 8:
        win_flag = "B"
        if dropper == "B":
            win_flag = "A"

    # known adjustment
    if dropper == "A" and drop == 2 and not hmaid_flag:
        A_knows = B[0]
    elif dropper == "B" and drop == 2 and not hmaid_flag:
        B_knows = A[0]
    elif drop == 6 and not hmaid_flag:
        A_knows = B[0]
        B_knows = A[0]

    # returning with hmaid_flag updated, known_flag updated
    return A, B, CARDS, drop == 4, A_knows, B_knows, win_flag, new_drop
