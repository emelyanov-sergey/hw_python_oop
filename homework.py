import typing
from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: int
    distance: int
    speed: float
    calories: float
    MESSAGE: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Вывод сообщения на экран о тренировке.   """
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60
    KMH_IN_MSEC: float = 0.278
    CM_IN_M: int = 100

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    COEF_1: int = 18
    COEF_2: float = 1.79

    def get_spent_calories(self) -> float:
        """Расчет затраченных калорий"""
        return (
            (self.COEF_1 * self.get_mean_speed() + self.COEF_2)
            * self.weight
            / self.M_IN_KM
            * (self.duration * self.MIN_IN_H)
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Расчет затраченных калорий"""
        return (
            self.CALORIES_WEIGHT_MULTIPLIER * self.weight
            + ((self.get_mean_speed() * self.KMH_IN_MSEC) ** 2
               / (self.height / self.CM_IN_M))
            * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
            * self.weight
        ) * (self.duration * self.MIN_IN_H)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    CALORIES_COTF_5: float = 1.1
    CALORIES_COTF_6: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость в бассейне"""
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Расчет затраченных калорий"""
        return ((self.get_mean_speed() + self.CALORIES_COTF_5)
                * self.CALORIES_COTF_6 * self.weight
                * self.duration)


def read_package(workout_type: str, data: typing.List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    data_of_training = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    if workout_type not in data_of_training:
        raise KeyError(f'Не верный тип тренировки - {workout_type}')
    return data_of_training[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
