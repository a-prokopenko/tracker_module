from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, Type


@dataclass
class InfoMessage:
    """Класс для создания объектов сообщений."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message: str = ('Тип тренировки: {training_type};'
                    ' Длительность: {duration:.3f} ч.;'
                    ' Дистанция: {distance:.3f} км;'
                    ' Ср. скорость: {speed:.3f} км/ч;'
                    ' Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.message.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float
    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000
    MIN_IN_HOUR: ClassVar[int] = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_RUN_1: ClassVar[int] = 18
    CALORIES_RUN_2: ClassVar[int] = 20

    def get_spent_calories(self) -> float:
        return (((self.CALORIES_RUN_1 * self.get_mean_speed()
                 - self.CALORIES_RUN_2) * self.weight)
                / self.M_IN_KM * self.duration * self.MIN_IN_HOUR)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float
    CALORIES_WLK_1: ClassVar[float] = 0.035
    CALORIES_WLK_2: ClassVar[float] = 0.029

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_WLK_1 * self.weight
                + (self.get_distance()**2 // self.height)
                * self.CALORIES_WLK_2 * self.weight)
                * self.duration * self.MIN_IN_HOUR)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: float
    count_pool: int
    LEN_STEP: ClassVar[float] = 1.38
    CALORIES_SWIM_1: ClassVar[float] = 1.1
    CALORIES_SWIM_2: ClassVar[int] = 2

    def get_mean_speed(self) -> float:
        total_length_pool = self.length_pool * self.count_pool
        return total_length_pool / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.CALORIES_SWIM_1)
                * self.CALORIES_SWIM_2 * self.weight)


def read_package(training_type: str, info: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_dict: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return type_dict[training_type](*info)


def main(workout: Training) -> None:
    """Главная функция."""
    info = workout.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
        ('NOT_VALID_KEY', [])
    ]

    for workout_type, data in packages:
        try:
            training = read_package(workout_type, data)
            main(training)
        except (KeyError, TypeError, AttributeError):
            print('Тренировка не найдена')
