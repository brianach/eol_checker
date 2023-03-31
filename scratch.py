    for hw_list1, hw_list2 in zip(INV_EOL, INVENTORY[:-1]):

        hw_items = [hw_item for hw_item in hw_list1 if hw_item in hw_list2]

        for i, hw_item in enumerate(hw_list2):
            ID_COUNT = hw_list2[-1][1:4]
            hw_type = hw_list2[0][0]
            if hw_item in hw_items:
                hw_item_idx = hw_list2.index(hw_item)
                hw_list2.pop(hw_item_idx)
                hw_list2.append(hw_type+str(ID_COUNT + 1).zfill(3)+date.today().strftime("%d%m%Y"))