def calculate_check_digit(data):
    try:
        if not data.isdigit():
            raise ValueError("データは数字のみで構成される必要があります")
        nums = [int(c) for c in data]
        odd_sum = sum(nums[-1::-2])
        even_sum = sum(nums[-2::-2])
        total = odd_sum * 3 + even_sum
        check_digit = (10 - total % 10) % 10
        return str(check_digit)
    except ValueError as e:
        return str(e)
    except Exception as e:
        return str(e)
