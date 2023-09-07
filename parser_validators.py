import argparse


class CommandValidator(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values not in ["new", "list"]:
            parser.error("Please, enter a valid command ('new or 'list')")
        setattr(namespace, self.dest, values)


class TypeValidator(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values not in ["education", "recreational", "social", "diy", "charity", "cooking", "relaxation", "music",
                         "busywork"]:
            raise argparse.ArgumentError(self, "Not a valid type entered!")
        setattr(namespace, self.dest, values)


class ParticipantsValidator(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values < 1:
            raise argparse.ArgumentError(self, "Invalid participants, please use a positive integer")
        setattr(namespace, self.dest, values)


class PriceValidator(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values < 0 or values > 1:
            raise argparse.ArgumentError(self, "Invalid price range, please use numbers between 0 and 1")
        setattr(namespace, self.dest, values)


class AccessibilityValidator(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values < 0 or values > 1:
            raise argparse.ArgumentError(self, "Invalid accessibility range, please use numbers between 0 and 1")
        setattr(namespace, self.dest, values)