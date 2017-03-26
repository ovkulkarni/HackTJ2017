class ConditionBlock:
    in_val = None
    out_val = None
    check = None

    def evaluate(self, context):
        if self.check == 'in':
            return self.in_val.format(**context) in self.out_val.format(**context)

