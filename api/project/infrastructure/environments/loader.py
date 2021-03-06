import errno
from os import path, strerror
from project.infrastructure.monitoring_layer.aplication_general_log import Log
import yaml


log = Log()

base_path = "./project/infrastructure/environments/config.yaml"


class Configs(object):
    @staticmethod
    def get_by_key(key, config_path: str = base_path) -> dict:
        """
            Busca uma configuralção baseado em uma chave e/ou
        caminho alternativo

        Args:
            key: string
            config_path (str, optional): Caminho alternativo
        valor padrão: basepath

        Raises:
            error: FileNotFoundError
            error: Exception

        Returns:
            environments: dict
        """

        try:

            path_exists = path.exists(config_path)

            if not path_exists:

                error = FileNotFoundError(
                    errno.ENOENT, strerror(errno.ENOENT), config_path
                )

                log.record.error(
                    "environments connection error, check environments config",
                    exc_info=error,
                )
                raise error

            with open(config_path, "r") as stream:
                config_dict = yaml.safe_load(stream)
                environments = config_dict["environments"]
                return environments[key] if key in environments else {}

        except Exception as error:
            log.record.error(
                "environments connection error, check environments config",
                exc_info=error,
            )
            raise error
