# Python 

## Dataclass 

```python
from abc import ABC, abstractmethod
from dataclasses import asdict, astuple, dataclass, field
from typing import Self


@dataclass
class User:
    name: str
    email: str
    age: int = 0
    tags: list[str] = field(default_factory=list[str])  # safe default field
    slug: str = field(init=False)

    def __post_init__(self):
        self.name = self.name.strip().title()
        slugified = self.name.lower().replace(" ", "-")
        self.slug = slugified

    @classmethod
    def from_email(self, email) -> Self:
        local = email.split("@")[0].replace(".", " ")
        return self(name=local, email=email)

    @property
    def domain(self) -> str:
        return self.email.split("@")[-1]


users: list[User] = [
    User(name="Alice Smith", age=28, email="alice@mail.com"),
    User(name="Bob", age=25, email="bob@mail.com"),
    User(name="Judit Polgár", age=29, email="judit@mail.com"),
    User.from_email("john.smith@mail.com"),
]

print(f"{users[0]=}")
print(f"{users[1]=}")
print(f"{users[2]=}")
print(f"{users[3]=}")

print(asdict(users[3]))
print(astuple(users[3]))


@dataclass
class Account(ABC):
    owner: str
    base_fee: float

    @property
    @abstractmethod
    def monthly_fee(self) -> float:
        pass


@dataclass
class FreeAccount(Account):
    @property
    def monthly_fee(self) -> float:
        return 0.0


@dataclass
class PremiumAccount(Account):
    extra_storage_gb: int = 100

    @property
    def monthly_fee(self) -> float:
        return self.base_fee + (self.extra_storage_gb * 0.10)


free_account = FreeAccount(owner="Aleksy", base_fee=10)
premium_account = PremiumAccount(owner="Wioletta", base_fee=20, extra_storage_gb=50)

print(f"{free_account=}")
print(f"{premium_account=}")
```

```python
# output
users[0]=User(name='Alice Smith', email='alice@mail.com', age=28, tags=[], slug='alice-smith')
users[1]=User(name='Bob', email='bob@mail.com', age=25, tags=[], slug='bob')
users[2]=User(name='Judit Polgár', email='judit@mail.com', age=29, tags=[], slug='judit-polgár')
users[3]=User(name='John Smith', email='john.smith@mail.com', age=0, tags=[], slug='john-smith')

{'name': 'John Smith', 'email': 'john.smith@mail.com', 'age': 0, 'tags': [], 'slug': 'john-smith'}
('John Smith', 'john.smith@mail.com', 0, [], 'john-smith')

free_account=FreeAccount(owner='Aleksy', base_fee=10)
premium_account=PremiumAccount(owner='Wioletta', base_fee=20, extra_storage_gb=50)
```
